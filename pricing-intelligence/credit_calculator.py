#!/usr/bin/env python3
"""Reproducible Salesforce Flex Credit *estimate*, not a quote (stdlib only)."""
import argparse
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

DEFAULT_RATES = Path(__file__).resolve().parent / "data" / "rate-card-2026-11-03.json"

def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, str, Decimal)):
        raise ValueError(f"{name}: use an integer or decimal string, not a float")
    try:
        out = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{name}: invalid number") from exc
    if not out.is_finite() or out < 0:
        raise ValueError(f"{name}: value must be finite and nonnegative")
    return out

def fmt(value):
    return format(value, "f")

def credit_units(quantity, meter):
    return quantity / number(meter["unit_size"], "unit_size")

def tiered_credits(units, multipliers, thresholds):
    """Thresholds are cumulative *credits*, for each meter per calendar month."""
    consumed = Decimal("0")
    rest = units
    rates = [number(x, "multiplier") for x in multipliers]
    limits = [number(x, "tier threshold") for x in thresholds]
    if len(rates) != len(limits) + 1:
        raise ValueError("rate card has wrong number of tiers")
    breakdown = []
    for i, rate in enumerate(rates):
        if rest == 0:
            break
        if rate <= 0:
            raise ValueError("tier multiplier must be positive")
        cap = (limits[i] - consumed) if i < len(limits) else None
        if cap is not None and cap < 0:
            raise ValueError("tier thresholds not increasing")
        take = rest if cap is None else min(rest, cap / rate)
        used = take * rate
        consumed += used
        rest -= take
        breakdown.append({"tier": i + 1, "meter_units": fmt(take), "credits": fmt(used)})
    if rest != 0:
        raise ValueError("tiered usage not fully allocated")
    return consumed, breakdown

def meter_catalog(rate_card):
    """Tool-discoverable meter metadata; no implicit source-price extrapolation."""
    return {
        "contract_version": "1.0",
        "rate_card_version": rate_card["rate_card_version"],
        "source_url": rate_card["source_url"],
        "review_status": rate_card.get("status", "UNKNOWN"),
        "meters": [
            {"id": meter_id, "unit": meter["unit"], "unit_size": meter["unit_size"],
             "environments": {
                 env: ("TIERED" if env == "production" and "production_tiers" in meter
                       else "AVAILABLE" if meter.get(env) is not None else "UNPRICEABLE")
                 for env in ("production", "sandbox")}}
            for meter_id, meter in sorted(rate_card["rate_meters"].items())
        ]
    }


def calculate(scenario, rate_card):
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be a JSON object")
    allowed = {"scenario_id", "scenario_name", "pricing_model", "usage",
               "included_credits", "allowance_source"}
    unknown = set(scenario) - allowed
    if unknown:
        raise ValueError(f"unsupported scenario fields: {sorted(unknown)}")
    if scenario.get("pricing_model") != "FLEX_CREDITS":
        raise ValueError("Only FLEX_CREDITS scenarios supported; Conversations cannot be combined here")
    raw = scenario.get("usage")
    if not isinstance(raw, list) or not raw:
        raise ValueError("usage must contain at least one record")
    rates = rate_card["rate_meters"]
    grouped = defaultdict(lambda: Decimal("0"))
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"usage[{i}]: expected object")
        unexpected = set(item) - {"month", "meter", "environment", "quantity"}
        if unexpected:
            raise ValueError(f"usage[{i}]: unsupported fields {sorted(unexpected)}")
        key = (item.get("month"), item.get("meter"), item.get("environment"))
        month, meter, environment = key
        if not isinstance(month, str) or not re.fullmatch(r"20[0-9]{2}-(0[1-9]|1[0-2])", month):
            raise ValueError(f"usage[{i}]: month must be YYYY-MM")
        if meter not in rates:
            raise ValueError(f"usage[{i}]: unknown meter {meter!r}")
        if environment not in ("production", "sandbox"):
            raise ValueError(f"usage[{i}]: environment must be production or sandbox")
        grouped[key] += number(item.get("quantity"), f"usage[{i}].quantity")

    priced = Decimal("0")
    lines, unpriceable = [], []
    for (month, meter_id, environment), quantity in sorted(grouped.items()):
        meter = rates[meter_id]
        units = credit_units(quantity, meter)
        if environment == "production" and "production_tiers" in meter:
            credits, tiers = tiered_credits(units, meter["production_tiers"], rate_card["data360_tier_thresholds_credits"])
        else:
            multiplier = meter.get(environment)
            if multiplier is None:
                unpriceable.append({"month": month, "meter": meter_id, "environment": environment,
                                    "quantity": fmt(quantity), "reason": meter.get("rate_status", "UNKNOWN_MULTIPLIER")})
                continue
            credits = units * number(multiplier, f"{meter_id}.{environment}")
            tiers = None
        priced += credits
        lines.append({"month": month, "meter": meter_id, "environment": environment,
                      "quantity": fmt(quantity), "unit": meter["unit"], "credits": fmt(credits),
                      "tier_breakdown": tiers, "source_url": rate_card["source_url"]})

    allowance = number(scenario.get("included_credits", "0"), "included_credits")
    if allowance > 0 and not scenario.get("allowance_source"):
        raise ValueError("Nonzero included_credits requires allowance_source")
    net = max(priced - allowance, Decimal("0"))
    list_rate = rate_card["list_price"]
    equivalent = net * number(list_rate["amount"], "list price") / number(list_rate["per_credits"], "credit denominator")
    equivalent = equivalent.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return {
        "contract_version": "1.0",
        "scenario_id": scenario.get("scenario_id"),
        "scenario_name": scenario.get("scenario_name"),
        "rate_card_review_status": rate_card.get("status", "UNKNOWN"),
        "status": "INCOMPLETE_UNPRICEABLE_USAGE" if unpriceable else "ESTIMATE_NOT_QUOTE",
        "rate_card_version": rate_card["rate_card_version"],
        "rate_card_source": rate_card["source_url"],
        "list_price_source": list_rate["source_url"],
        "priced_lines": lines,
        "unpriceable_usage": unpriceable,
        "priced_credits_only": fmt(priced),
        "allowance_assumption": fmt(allowance),
        "net_priced_credits_only": fmt(net),
        "partial_list_price_equivalent": {"amount": fmt(equivalent), "currency": list_rate["currency"]},
        "note": "Partial if any unpriceable meter; list-price equivalent is not a pack purchase, invoice, or approved quote."
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", help="Scenario JSON path, or '-' for stdin")
    parser.add_argument("--list-meters", action="store_true", help="Return JSON meter catalog for agents")
    parser.add_argument("--rates", type=Path, default=DEFAULT_RATES)
    args = parser.parse_args()
    if not args.list_meters and not args.scenario:
        parser.error("provide --scenario PATH/- or --list-meters")
    try:
        rate_card = json.loads(args.rates.read_text(encoding="utf-8"))
        if args.list_meters:
            output = meter_catalog(rate_card)
        else:
            raw = sys.stdin.read() if args.scenario == "-" else Path(args.scenario).read_text(encoding="utf-8")
            output = calculate(json.loads(raw), rate_card)
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
