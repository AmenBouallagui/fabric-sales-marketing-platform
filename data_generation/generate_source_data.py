"""Generate deterministic synthetic source data for the Fabric portfolio project."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from faker import Faker


CHANNELS = [
    "Paid Search",
    "Paid Social",
    "Organic",
    "Email",
    "Referral",
    "Partner",
    "Direct",
]

COUNTRY_CITIES = {
    "United States": ["New York", "Austin", "Seattle", "Chicago", "San Francisco"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Bristol", "Edinburgh"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Lille"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven", "The Hague"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
}

INDUSTRIES = [
    "Technology",
    "Financial Services",
    "Healthcare",
    "Retail",
    "Manufacturing",
    "Education",
    "Professional Services",
    "Media",
    "Logistics",
    "Telecommunications",
]

SEGMENTS = ["Enterprise", "Mid-Market", "SMB", "Startup"]
COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-1000", "1001-5000", "5000+"]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the generator."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic source CSV files for the Fabric portfolio project."
    )
    parser.add_argument("--output-dir", default="data/source", help="Output folder for CSV files.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic output.")
    parser.add_argument("--customers", type=int, default=1000, help="Number of customer rows.")
    parser.add_argument("--orders", type=int, default=10000, help="Number of order rows.")
    parser.add_argument("--start-date", default="2024-01-01", help="Inclusive data start date.")
    parser.add_argument("--end-date", default="2025-12-31", help="Inclusive data end date.")
    return parser.parse_args()


def random_dates(
    rng: np.random.Generator,
    start: pd.Timestamp,
    end: pd.Timestamp,
    count: int,
) -> pd.Series:
    """Return deterministic random dates between start and end, inclusive."""
    day_span = max((end - start).days, 0)
    offsets = rng.integers(0, day_span + 1, size=count)
    return pd.Series(start + pd.to_timedelta(offsets, unit="D"))


def add_days(
    rng: np.random.Generator,
    dates: pd.Series,
    min_days: int,
    max_days: int,
) -> pd.Series:
    """Add a deterministic random day offset to a series of dates."""
    offsets = rng.integers(min_days, max_days + 1, size=len(dates))
    return dates + pd.to_timedelta(offsets, unit="D")


def generate_customers(
    count: int,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    rng: np.random.Generator,
    faker: Faker,
) -> pd.DataFrame:
    """Generate synthetic customer master data."""
    countries = rng.choice(list(COUNTRY_CITIES.keys()), size=count)
    cities = [rng.choice(COUNTRY_CITIES[country]) for country in countries]
    signup_dates = random_dates(rng, start_date, end_date, count)
    statuses = rng.choice(["Active", "Inactive", "Churned"], size=count, p=[0.86, 0.10, 0.04])
    segments = rng.choice(SEGMENTS, size=count, p=[0.18, 0.30, 0.38, 0.14])

    names = [faker.company() for _ in range(count)]
    email_domains = [name.lower().replace(",", "").replace(" ", "")[:18] for name in names]
    emails = [f"contact{i + 1}@{domain}.example" for i, domain in enumerate(email_domains)]

    customers = pd.DataFrame(
        {
            "customer_id": [f"CUST-{i:06d}" for i in range(1, count + 1)],
            "account_id": [f"ACC-{i:06d}" for i in range(1, count + 1)],
            "customer_name": names,
            "email": emails,
            "country": countries,
            "city": cities,
            "signup_date": signup_dates,
            "acquisition_channel": rng.choice(
                CHANNELS, size=count, p=[0.20, 0.18, 0.16, 0.16, 0.10, 0.12, 0.08]
            ),
            "customer_segment": segments,
            "company_size": rng.choice(COMPANY_SIZES, size=count, p=[0.10, 0.18, 0.26, 0.24, 0.14, 0.08]),
            "industry": rng.choice(INDUSTRIES, size=count),
            "status": statuses,
            "updated_at": add_days(rng, signup_dates, 0, 90),
        }
    )
    return customers


def generate_products(
    start_date: pd.Timestamp,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic product catalog data."""
    product_specs = [
        ("Sales Insights Starter", "Analytics", "Starter", 49.0, True),
        ("Sales Insights Pro", "Analytics", "Professional", 149.0, True),
        ("Revenue Intelligence", "Analytics", "Enterprise", 399.0, True),
        ("Campaign Optimizer", "Marketing", "Professional", 199.0, True),
        ("Lead Scoring API", "AI Services", "Enterprise", 499.0, True),
        ("Customer 360 Export", "Data Services", "Starter", 79.0, True),
        ("Data Quality Monitor", "Governance", "Professional", 249.0, True),
        ("Attribution Model Pack", "Marketing", "Enterprise", 599.0, False),
        ("Pipeline Forecast Add-On", "AI Services", "Professional", 299.0, True),
        ("Executive Dashboard Pack", "Reporting", "Starter", 129.0, False),
        ("Partner Portal Connector", "Integration", "Enterprise", 699.0, True),
        ("CRM Sync Connector", "Integration", "Professional", 189.0, True),
    ]

    rows = []
    for index, (name, category, tier, price, subscription) in enumerate(product_specs, start=1):
        valid_from = start_date - pd.Timedelta(days=int(rng.integers(30, 365)))
        valid_to = pd.NaT if rng.random() > 0.18 else start_date + pd.Timedelta(days=int(rng.integers(180, 720)))
        unit_cost = round(price * float(rng.uniform(0.28, 0.52)), 2)
        rows.append(
            {
                "product_id": f"PROD-{index:03d}",
                "product_name": name,
                "category": category,
                "plan_tier": tier,
                "unit_price": round(price, 2),
                "unit_cost": unit_cost,
                "is_subscription": subscription,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "updated_at": valid_from + pd.Timedelta(days=int(rng.integers(0, 30))),
            }
        )
    return pd.DataFrame(rows)


def generate_campaigns(
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic marketing campaign data."""
    objectives = ["Awareness", "Lead Generation", "Conversion", "Retention", "Expansion"]
    campaign_count = 36
    starts = random_dates(rng, start_date - pd.Timedelta(days=45), end_date, campaign_count)
    durations = rng.integers(21, 121, size=campaign_count)
    ends = starts + pd.to_timedelta(durations, unit="D")

    ongoing_mask = rng.random(campaign_count) < 0.18
    ends = ends.mask(ongoing_mask, pd.NaT)

    channels = rng.choice(CHANNELS, size=campaign_count, p=[0.24, 0.22, 0.12, 0.18, 0.08, 0.10, 0.06])
    objectives_chosen = rng.choice(objectives, size=campaign_count)
    target_segments = rng.choice(SEGMENTS, size=campaign_count)

    campaigns = pd.DataFrame(
        {
            "campaign_id": [f"CMP-{i:04d}" for i in range(1, campaign_count + 1)],
            "campaign_name": [
                f"{channel} {objective} {start.year} Q{((start.month - 1) // 3) + 1}"
                for channel, objective, start in zip(channels, objectives_chosen, starts)
            ],
            "channel": channels,
            "campaign_start_date": starts,
            "campaign_end_date": ends,
            "target_segment": target_segments,
            "objective": objectives_chosen,
            "updated_at": starts + pd.to_timedelta(rng.integers(0, 21, size=campaign_count), unit="D"),
        }
    )
    ended = campaigns["campaign_end_date"].notna()
    campaigns.loc[ended, "updated_at"] = campaigns.loc[ended, ["updated_at", "campaign_end_date"]].max(axis=1)
    return campaigns


def generate_orders(
    count: int,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    campaigns: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic order transactions linked to customers, products, and campaigns."""
    customer_indices = rng.integers(0, len(customers), size=count)
    product_indices = rng.integers(0, len(products), size=count)
    selected_customers = customers.iloc[customer_indices].reset_index(drop=True)
    selected_products = products.iloc[product_indices].reset_index(drop=True)

    order_dates = []
    for signup_date in selected_customers["signup_date"]:
        lower_bound = max(pd.Timestamp(signup_date), start_date)
        order_dates.append(random_dates(rng, lower_bound, end_date, 1).iloc[0])
    order_dates_series = pd.Series(order_dates)

    quantities = rng.choice([1, 1, 1, 2, 2, 3, 4, 5], size=count)
    unit_prices = selected_products["unit_price"].astype(float).to_numpy()
    subtotal = unit_prices * quantities
    discount_rates = rng.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=count, p=[0.55, 0.16, 0.14, 0.10, 0.05])
    discount_amount = np.round(subtotal * discount_rates, 2)
    taxable_amount = subtotal - discount_amount
    tax_amount = np.round(taxable_amount * 0.08, 2)
    total_amount = np.round(taxable_amount + tax_amount, 2)

    payment_status = rng.choice(["Paid", "Failed", "Pending"], size=count, p=[0.91, 0.04, 0.05])
    refund_flag = rng.random(count) < 0.035
    campaign_ids = rng.choice(campaigns["campaign_id"].to_numpy(), size=count)
    has_campaign = rng.random(count) < 0.62
    campaign_ids = np.where(has_campaign, campaign_ids, None)

    orders = pd.DataFrame(
        {
            "order_id": [f"ORD-{i:08d}" for i in range(1, count + 1)],
            "customer_id": selected_customers["customer_id"].to_numpy(),
            "product_id": selected_products["product_id"].to_numpy(),
            "order_date": order_dates_series,
            "quantity": quantities,
            "unit_price": np.round(unit_prices, 2),
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "payment_status": payment_status,
            "refund_flag": refund_flag,
            "campaign_id": campaign_ids,
            "updated_at": add_days(rng, order_dates_series, 0, 45),
        }
    )
    return orders


def generate_ad_spend(
    campaigns: pd.DataFrame,
    end_date: pd.Timestamp,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic daily ad spend linked to campaigns."""
    rows = []
    paid_channels = {"Paid Search", "Paid Social", "Email", "Partner", "Referral", "Organic", "Direct"}
    spend_id = 1

    for campaign in campaigns.itertuples(index=False):
        start = pd.Timestamp(campaign.campaign_start_date)
        campaign_end = pd.Timestamp(campaign.campaign_end_date) if pd.notna(campaign.campaign_end_date) else end_date
        campaign_end = min(campaign_end, end_date)
        if campaign_end < start:
            continue

        active_days = pd.date_range(start=start, end=campaign_end, freq="D")
        sample_size = min(len(active_days), int(rng.integers(12, 46)))
        selected_days = rng.choice(active_days.to_numpy(), size=sample_size, replace=False)

        for spend_date_value in sorted(selected_days):
            spend_date = pd.Timestamp(spend_date_value)
            base_spend = float(rng.uniform(80, 2400)) if campaign.channel in paid_channels else float(rng.uniform(25, 400))
            impressions = int(max(base_spend * rng.uniform(35, 120), 100))
            clicks = int(max(impressions * rng.uniform(0.008, 0.075), 1))
            conversions = int(max(clicks * rng.uniform(0.015, 0.16), 0))
            rows.append(
                {
                    "spend_id": f"SPEND-{spend_id:07d}",
                    "campaign_id": campaign.campaign_id,
                    "spend_date": spend_date,
                    "channel": campaign.channel,
                    "impressions": impressions,
                    "clicks": clicks,
                    "conversions": conversions,
                    "spend_amount": round(base_spend, 2),
                    "updated_at": spend_date + pd.Timedelta(days=int(rng.integers(0, 10))),
                }
            )
            spend_id += 1

    return pd.DataFrame(rows)


def generate_support_tickets(
    customers: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate synthetic support tickets linked to customers."""
    ticket_count = max(int(len(customers) * 1.45), 250)
    customer_indices = rng.integers(0, len(customers), size=ticket_count)
    selected_customers = customers.iloc[customer_indices].reset_index(drop=True)

    created_dates = []
    for signup_date in selected_customers["signup_date"]:
        lower_bound = max(pd.Timestamp(signup_date), start_date)
        created_dates.append(random_dates(rng, lower_bound, end_date, 1).iloc[0])
    created_at = pd.Series(created_dates) + pd.to_timedelta(rng.integers(0, 24 * 60, size=ticket_count), unit="m")

    priorities = rng.choice(["Low", "Medium", "High", "Critical"], size=ticket_count, p=[0.38, 0.42, 0.16, 0.04])
    categories = rng.choice(
        ["Billing", "Login", "Data Sync", "Reporting", "Product Question", "Integration", "Performance"],
        size=ticket_count,
    )
    statuses = rng.choice(["Closed", "Resolved", "Open", "In Progress"], size=ticket_count, p=[0.54, 0.28, 0.10, 0.08])
    is_open = np.isin(statuses, ["Open", "In Progress"])

    first_response = rng.integers(5, 8 * 60, size=ticket_count)
    resolution = first_response + rng.integers(30, 7 * 24 * 60, size=ticket_count)
    closed_at = created_at + pd.to_timedelta(resolution, unit="m")
    closed_at = closed_at.mask(is_open, pd.NaT)

    satisfaction = rng.integers(1, 6, size=ticket_count).astype("float")
    satisfaction[is_open] = np.nan
    resolution_minutes = resolution.astype("float")
    resolution_minutes[is_open] = np.nan

    tickets = pd.DataFrame(
        {
            "ticket_id": [f"TCK-{i:07d}" for i in range(1, ticket_count + 1)],
            "customer_id": selected_customers["customer_id"].to_numpy(),
            "created_at": created_at,
            "closed_at": closed_at,
            "priority": priorities,
            "category": categories,
            "status": statuses,
            "satisfaction_score": satisfaction,
            "first_response_minutes": first_response,
            "resolution_minutes": resolution_minutes,
            "updated_at": created_at + pd.to_timedelta(rng.integers(0, 30 * 24 * 60, size=ticket_count), unit="m"),
        }
    )
    closed_mask = tickets["closed_at"].notna()
    tickets.loc[closed_mask, "updated_at"] = tickets.loc[closed_mask, ["updated_at", "closed_at"]].max(axis=1)
    return tickets


def validate_data(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    campaigns: pd.DataFrame,
    orders: pd.DataFrame,
    ad_spend: pd.DataFrame,
    support_tickets: pd.DataFrame,
) -> None:
    """Validate generated relational integrity, monetary values, and primary keys."""
    checks = [
        ("customers.customer_id", customers, "customer_id"),
        ("products.product_id", products, "product_id"),
        ("campaigns.campaign_id", campaigns, "campaign_id"),
        ("orders.order_id", orders, "order_id"),
        ("ad_spend.spend_id", ad_spend, "spend_id"),
        ("support_tickets.ticket_id", support_tickets, "ticket_id"),
    ]
    for label, frame, column in checks:
        if frame[column].isna().any() or not frame[column].is_unique:
            raise ValueError(f"Required ID column is not unique and complete: {label}")

    customer_ids = set(customers["customer_id"])
    product_ids = set(products["product_id"])
    campaign_ids = set(campaigns["campaign_id"])

    if not set(orders["customer_id"]).issubset(customer_ids):
        raise ValueError("orders.customer_id contains values missing from customers.")
    if not set(orders["product_id"]).issubset(product_ids):
        raise ValueError("orders.product_id contains values missing from products.")

    order_campaigns = set(orders["campaign_id"].dropna())
    if not order_campaigns.issubset(campaign_ids):
        raise ValueError("orders.campaign_id contains values missing from campaigns.")
    if not set(ad_spend["campaign_id"]).issubset(campaign_ids):
        raise ValueError("ad_spend.campaign_id contains values missing from campaigns.")
    if not set(support_tickets["customer_id"]).issubset(customer_ids):
        raise ValueError("support_tickets.customer_id contains values missing from customers.")

    money_checks = {
        "products.unit_price": products["unit_price"],
        "products.unit_cost": products["unit_cost"],
        "orders.unit_price": orders["unit_price"],
        "orders.discount_amount": orders["discount_amount"],
        "orders.tax_amount": orders["tax_amount"],
        "orders.total_amount": orders["total_amount"],
        "ad_spend.spend_amount": ad_spend["spend_amount"],
    }
    for label, values in money_checks.items():
        if (values < 0).any():
            raise ValueError(f"Negative monetary values found in {label}.")

    expected_total = (
        orders["unit_price"] * orders["quantity"] - orders["discount_amount"] + orders["tax_amount"]
    ).round(2)
    if not np.allclose(orders["total_amount"], expected_total):
        raise ValueError("orders.total_amount is not consistent with price, quantity, discount, and tax.")

    chronology_checks = [
        ("customers.updated_at", customers["updated_at"], customers["signup_date"]),
        ("products.updated_at", products["updated_at"], products["valid_from"]),
        ("campaigns.updated_at", campaigns["updated_at"], campaigns["campaign_start_date"]),
        ("orders.updated_at", orders["updated_at"], orders["order_date"]),
        ("ad_spend.updated_at", ad_spend["updated_at"], ad_spend["spend_date"]),
        ("support_tickets.updated_at", support_tickets["updated_at"], support_tickets["created_at"]),
    ]
    for label, updated_at, event_date in chronology_checks:
        if (updated_at < event_date).any():
            raise ValueError(f"{label} contains values earlier than the related business event date.")


def format_dates(frames: Iterable[pd.DataFrame]) -> None:
    """Format datetime columns consistently before writing CSV files."""
    for frame in frames:
        for column in frame.columns:
            if pd.api.types.is_datetime64_any_dtype(frame[column]):
                if column.endswith("_at"):
                    frame[column] = frame[column].dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    frame[column] = frame[column].dt.strftime("%Y-%m-%d")


def write_csvs(output_dir: Path, datasets: dict[str, pd.DataFrame]) -> None:
    """Write generated datasets to CSV files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, frame in datasets.items():
        frame.to_csv(output_dir / filename, index=False)


def main() -> None:
    """Run the synthetic source data generation workflow."""
    args = parse_args()
    start_date = pd.Timestamp(args.start_date)
    end_date = pd.Timestamp(args.end_date)
    if end_date < start_date:
        raise ValueError("--end-date must be equal to or later than --start-date.")
    if args.customers <= 0 or args.orders <= 0:
        raise ValueError("--customers and --orders must be positive integers.")

    rng = np.random.default_rng(args.seed)
    faker = Faker()
    faker.seed_instance(args.seed)

    customers = generate_customers(args.customers, start_date, end_date, rng, faker)
    products = generate_products(start_date, rng)
    campaigns = generate_campaigns(start_date, end_date, rng)
    orders = generate_orders(args.orders, customers, products, campaigns, start_date, end_date, rng)
    ad_spend = generate_ad_spend(campaigns, end_date, rng)
    support_tickets = generate_support_tickets(customers, start_date, end_date, rng)

    validate_data(customers, products, campaigns, orders, ad_spend, support_tickets)

    datasets = {
        "customers.csv": customers,
        "products.csv": products,
        "campaigns.csv": campaigns,
        "orders.csv": orders,
        "ad_spend.csv": ad_spend,
        "support_tickets.csv": support_tickets,
    }
    format_dates(datasets.values())
    write_csvs(Path(args.output_dir), datasets)

    print("Synthetic source data generated successfully.")
    print(f"Output path: {Path(args.output_dir).resolve()}")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print(f"Seed: {args.seed}")
    for filename, frame in datasets.items():
        print(f"{filename}: {len(frame):,} rows")


if __name__ == "__main__":
    main()
