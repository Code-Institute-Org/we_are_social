#!/usr/bin/env bash
curl -H "Content-Type: application/json" -X POST -d '
{
  "object":
    {
        "id": "in_17j6BCK4oMdhkST3ArlcRYID",
        "object": "invoice",
        "amount_due": 999,
        "application_fee": null,
        "attempt_count": 1,
        "attempted": true,
        "charge": "ch_17j6BCK4oMdhkST3meBXlX06",
        "closed": true,
        "currency": "gbp",
        "customer": "cus_7z4J5DGrXLgbJP",
        "date": 1456572250,
        "description": null,
        "discount": null,
        "ending_balance": 0,
        "forgiven": false,
        "lines":
        {
            "object": "list",
            "data":[
                {
                    "id": "sub_7z4Juj7UIkWOGV",
                    "object": "line_item",
                    "amount": 999,
                    "currency": "gbp",
                    "description": null,
                    "discountable": true,
                    "livemode": false,
                    "metadata": {},
                    "period": {
                        "start": 1456517913,
                        "end": 1456604313
                    },
                    "plan": {
                        "id": "REG_MONTHLY_",
                        "object": "plan",
                        "amount": 999,
                        "created": 1456571797,
                        "currency": "gbp",
                        "interval": "month",
                        "interval_count": 1,
                        "livemode": false,
                        "metadata": {},
                        "name": "Monthly Subscription",
                        "statement_descriptor": null,
                        "trial_period_days": null
                    },
                    "proration": false,
                    "quantity": 1,
                    "subscription": null,
                    "type": "subscription"

                }
            ],
            "has_more": false,
            "total_count": 1,
            "url": "/v1/invoices/in_17j6BCK4oMdhkST3ArlcRYID/lines"

        },
        "livemode": false,
        "metadata":{
        },
        "next_payment_attempt": null,
        "paid": true,
        "period_end": 1456572250,
        "period_start": 1456572250,
        "receipt_number": null,
        "starting_balance": 0,
        "statement_descriptor": null,
        "subscription": "sub_7z4Juj7UIkWOGV",
        "subtotal": 999,
        "tax": null,
        "tax_percent": null,
        "total": 999,
        "webhooks_delivered_at": null

    }
}' http://localhost:8000/subscriptions_webhook/

