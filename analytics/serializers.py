from rest_framework import serializers


class AnalyticsSerializer(serializers.Serializer):

    # =====================================================
    # BASIC STATISTICS
    # =====================================================

    total_trades = serializers.IntegerField()

    winning_trades = serializers.IntegerField()

    losing_trades = serializers.IntegerField()

    breakeven_trades = serializers.IntegerField()

    win_rate = serializers.FloatField()

    gross_pnl = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    net_pnl = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    gross_profit = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    gross_loss = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    profit_factor = serializers.DecimalField(
        max_digits=20,
        decimal_places=4,
        allow_null=True,
    )

    average_win = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    average_loss = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    expectancy = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    largest_win = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    largest_loss = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    total_fees = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    # =====================================================
    # DRAWDOWN
    # =====================================================

    maximum_drawdown = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    current_drawdown = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    # =====================================================
    # EQUITY CURVE
    # =====================================================

    equity_curve = serializers.ListField()

    # =====================================================
    # TIME BASED P/L
    # =====================================================

    daily_pnl = serializers.ListField()

    weekly_pnl = serializers.ListField()

    monthly_pnl = serializers.ListField()

    yearly_pnl = serializers.ListField()

    # =====================================================
    # LONG VS SHORT
    # =====================================================

    long_vs_short = serializers.DictField()

    # =====================================================
    # SYMBOL / STRATEGY
    # =====================================================

    symbol_performance = serializers.ListField()

    strategy_performance = serializers.ListField()

    # =====================================================
    # RISK / REWARD
    # =====================================================

    average_rr = serializers.DecimalField(
        max_digits=20,
        decimal_places=4,
        allow_null=True,
    )

    r_multiple_analysis = serializers.DictField()

    # =====================================================
    # STREAKS
    # =====================================================

    winning_streak = serializers.IntegerField()

    losing_streak = serializers.IntegerField()

    # =====================================================
    # BEST / WORST DAY
    # =====================================================

    best_trading_day = serializers.DictField(
        allow_null=True,
    )

    worst_trading_day = serializers.DictField(
        allow_null=True,
    )

    # =====================================================
    # CALENDAR
    # =====================================================

    calendar_pnl = serializers.ListField()

    # =====================================================
    # FREQUENCY
    # =====================================================

    trade_frequency = serializers.DictField()

    # =====================================================
    # HOLDING TIME
    # =====================================================

    average_holding_time = serializers.DictField()

    # =====================================================
    # BEST / WORST SYMBOL
    # =====================================================

    best_performing_symbol = serializers.DictField(
        allow_null=True,
    )

    worst_performing_symbol = serializers.DictField(
        allow_null=True,
    )