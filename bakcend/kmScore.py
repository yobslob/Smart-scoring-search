class kmScore:
    def __init__(self, startup):
        self.startup = startup

    def score_monthly_revenue(self, x):
        if x < 500_000: return 0
        elif x <= 1_000_000: return 20
        elif x <= 2_500_000: return 40
        elif x <= 5_000_000: return 60
        elif x <= 7_500_000: return 80
        else: return 100

    def score_active_users(self, x):
        if x < 5_000: return 0
        elif x <= 10_000: return 20
        elif x <= 25_000: return 40
        elif x <= 50_000: return 60
        elif x <= 75_000: return 80
        else: return 100

    def score_cac(self, x):
        if x > 1000: return 0
        elif x > 700: return 20
        elif x > 500: return 40
        elif x > 300: return 60
        elif x > 200: return 80
        else: return 100

    def score_mrr(self, x):
        if x < 250_000: return 0
        elif x <= 750_000: return 20
        elif x <= 1_500_000: return 40
        elif x <= 2_500_000: return 60
        elif x <= 4_000_000: return 80
        else: return 100

    def score(self, weights=None): 
        if weights is None:
            weights = {
                'monthly_revenue_inr': 0.3,
                'active_users': 0.2,
                'cac_inr': 0.2,
                'mrr_inr': 0.3
            }

        s = self.startup

        score = 0
        score += weights['monthly_revenue_inr'] * self.score_monthly_revenue(s['monthly_revenue_inr'])
        score += weights['active_users'] * self.score_active_users(s['active_users'])
        score += weights['cac_inr'] * self.score_cac(s['cac_inr'])
        score += weights['mrr_inr'] * self.score_mrr(s['mrr_inr'])

        return round(score, 2)