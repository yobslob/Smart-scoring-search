import math
import logging

class kmScore:
    def __init__(self, metadata, stage_stats):
        self.metadata = metadata
        self.stage_stats = stage_stats

    def score(self):
        s = self.metadata
        stage = s.get('stage', '')
        key_metrics = s.get('key_metrics', {})
        industry = s.get('industry', '')
        funding_ask = s.get('funding_ask', {}).get('amount_inr', 0)

        # 1) Unified revenue mapping
        mrr   = key_metrics.get('mrr_inr', 0)
        mrev  = key_metrics.get('monthly_revenue_inr', 0)
        revenue = mrr if industry in ['SaaS', 'EdTech'] else mrev

        # 2) Basic metrics
        active_users = key_metrics.get('active_users', 0)
        cac          = key_metrics.get('cac_inr', 0)

        # 3) Proxy metrics
        rev_per_user = revenue / active_users if active_users > 0 else 0
        ueh_proxy    = rev_per_user / cac     if cac > 0 else 0
        payback_proxy= (cac / rev_per_user)   if rev_per_user > 0 else 1e6
        capeff_proxy = (revenue * 12) / funding_ask if funding_ask > 0 else 1e6

        # 4) Stage stats check
        if not self.stage_stats:
            logging.warning(f"No stats for stage '{stage}'")
            return 0

        means = self.stage_stats['mean']
        stds  = self.stage_stats['std']

        # 5) Z‑scoring (clamp proxies first)
        def zs(val, m, sd):
            return (val - m) / sd if sd > 0 else 0

        z_users    = zs(active_users, means['active_users'], stds['active_users'])
        z_revenue  = zs(revenue,      means['revenue'],      stds['revenue'])
        z_ueh      = zs(ueh_proxy,    means['ueh_proxy'],     stds['ueh_proxy'])
        z_payback  = -zs(min(payback_proxy, 1e6), means['payback_proxy'], stds['payback_proxy'])
        z_capeff   = -zs(min(capeff_proxy, 1e6),  means['capeff_proxy'],  stds['capeff_proxy'])

        # 6) Weights per stage
        weights = {
            'Pre-seed': {'users':0.4,'revenue':0.05,'ueh':0.2,'payback':0.05,'capeff':0.3},
            'Seed':     {'users':0.15,'revenue':0.25,'ueh':0.3,'payback':0.1,'capeff':0.2},
            'Growth':   {'users':0.1,'revenue':0.2,'ueh':0.25,'payback':0.15,'capeff':0.3},
            'Series A': {'users':0.05,'revenue':0.3,'ueh':0.2,'payback':0.2,'capeff':0.25},
            'Series B': {'users':0.05,'revenue':0.35,'ueh':0.15,'payback':0.25,'capeff':0.2},
        }
        if stage not in weights:
            logging.warning(f"Unknown stage '{stage}'")
            return 0

        w = weights[stage]
        composite = (
            z_users   * w['users']   +
            z_revenue * w['revenue'] +
            z_ueh     * w['ueh']     +
            z_payback * w['payback'] +
            z_capeff  * w['capeff']
        )

        # 7) Final 0–100 mapping
        score = 50 + 10 * composite
        return round(max(0, min(100, score)), 2)