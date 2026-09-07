from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from trades.models import Trade


ZERO = Decimal("0")


def decimal(value):
    if value is None:
        return ZERO

    return Decimal(str(value))


def trade_net_pnl(trade):
    """
    Net P/L for a trade.

    pnl  = gross trade P/L
    fees = trading costs
    """
    return decimal(trade.pnl) - decimal(trade.fees)


def get_user_trades(user):
    return Trade.objects.filter(
        user=user
    ).order_by("entry_time", "id")


# =========================================================
# BASIC STATISTICS
# =========================================================
def basic_statistics(trades):
    trade_list = list(trades)

    total_trades = len(trade_list)

    winning_trades = sum(
        1
        for trade in trade_list
        if trade_net_pnl(trade) > ZERO
    )

    losing_trades = sum(
        1
        for trade in trade_list
        if trade_net_pnl(trade) < ZERO
    )

    breakeven_trades = sum(
        1
        for trade in trade_list
        if trade_net_pnl(trade) == ZERO
    )

    gross_profit = sum(
        (
            trade_net_pnl(trade)
            for trade in trade_list
            if trade_net_pnl(trade) > ZERO
        ),
        ZERO,
    )

    gross_loss = sum(
        (
            trade_net_pnl(trade)
            for trade in trade_list
            if trade_net_pnl(trade) < ZERO
        ),
        ZERO,
    )

    total_fees = sum(
        (
            decimal(trade.fees)
            for trade in trade_list
        ),
        ZERO,
    )

    gross_pnl = sum(
        (
            decimal(trade.pnl)
            for trade in trade_list
        ),
        ZERO,
    )

    net_pnl = sum(
        (
            trade_net_pnl(trade)
            for trade in trade_list
        ),
        ZERO,
    )

    # Use Decimal instead of float for financial calculations.
    win_rate = (
        (
            Decimal(winning_trades)
            / Decimal(total_trades)
        ) * Decimal("100")
        if total_trades
        else ZERO
    )

    average_win = (
        gross_profit / Decimal(winning_trades)
        if winning_trades
        else ZERO
    )

    average_loss = (
        gross_loss / Decimal(losing_trades)
        if losing_trades
        else ZERO
    )

    average_loss_abs = abs(average_loss)

    profit_factor = (
        gross_profit / abs(gross_loss)
        if gross_loss < ZERO
        else None
    )

    # Expectancy = probability of win × average win
    #              - probability of loss × average loss
    if total_trades:
        win_probability = (
            Decimal(winning_trades)
            / Decimal(total_trades)
        )

        loss_probability = (
            Decimal(losing_trades)
            / Decimal(total_trades)
        )

        expectancy = (
            (win_probability * average_win)
            -
            (loss_probability * average_loss_abs)
        )
    else:
        expectancy = ZERO

    winning_values = [
        trade_net_pnl(trade)
        for trade in trade_list
        if trade_net_pnl(trade) > ZERO
    ]

    losing_values = [
        trade_net_pnl(trade)
        for trade in trade_list
        if trade_net_pnl(trade) < ZERO
    ]

    largest_win = (
        max(winning_values)
        if winning_values
        else ZERO
    )

    largest_loss = (
        min(losing_values)
        if losing_values
        else ZERO
    )

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "breakeven_trades": breakeven_trades,
        "win_rate": float(
            round(win_rate, 2)
        ),
        "gross_pnl": gross_pnl,
        "net_pnl": net_pnl,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": (
            round(profit_factor, 4)
            if profit_factor is not None
            else None
        ),
        "average_win": average_win,
        "average_loss": average_loss,
        "expectancy": expectancy,
        "largest_win": largest_win,
        "largest_loss": largest_loss,
        "total_fees": total_fees,
    }

# =========================================================
# EQUITY CURVE / DRAWDOWN
# =========================================================

def equity_curve(trades):
    equity = ZERO
    peak = ZERO

    maximum_drawdown = ZERO
    current_drawdown = ZERO

    result = []

    for trade in trades:
        net_pnl = trade_net_pnl(trade)

        equity += net_pnl

        if equity > peak:
            peak = equity

        drawdown = equity - peak

        if drawdown < maximum_drawdown:
            maximum_drawdown = drawdown

        current_drawdown = drawdown

        result.append({
            "trade_id": trade.id,
            "date": trade.entry_time,
            "pnl": decimal(trade.pnl),
            "fees": decimal(trade.fees),
            "net_pnl": net_pnl,
            "equity": equity,
            "drawdown": drawdown,
        })

    return {
        "data": result,
        "maximum_drawdown": maximum_drawdown,
        "current_drawdown": current_drawdown,
    }


# =========================================================
# DAILY / WEEKLY / MONTHLY / YEARLY P/L
# =========================================================

def group_pnl(trades, period):
    result = defaultdict(lambda: ZERO)

    for trade in trades:
        date = trade.entry_time
        net_pnl = trade_net_pnl(trade)

        if period == "daily":
            key = date.strftime("%Y-%m-%d")

        elif period == "weekly":
            iso = date.isocalendar()
            key = f"{iso.year}-W{iso.week:02d}"

        elif period == "monthly":
            key = date.strftime("%Y-%m")

        elif period == "yearly":
            key = date.strftime("%Y")

        else:
            continue

        result[key] += net_pnl

    return [
        {
            "period": key,
            "pnl": value,
        }
        for key, value in sorted(result.items())
    ]


# =========================================================
# LONG VS SHORT
# =========================================================

def direction_performance(trades):
    result = {}

    for direction in ["LONG", "SHORT"]:
        direction_trades = [
            trade
            for trade in trades
            if trade.direction == direction
        ]

        total = len(direction_trades)

        wins = sum(
            1
            for trade in direction_trades
            if trade_net_pnl(trade) > ZERO
        )

        losses = sum(
            1
            for trade in direction_trades
            if trade_net_pnl(trade) < ZERO
        )

        breakeven = sum(
            1
            for trade in direction_trades
            if trade_net_pnl(trade) == ZERO
        )

        net_pnl = sum(
            (
                trade_net_pnl(trade)
                for trade in direction_trades
            ),
            ZERO,
        )

        result[direction.lower()] = {
            "trades": total,
            "winning_trades": wins,
            "losing_trades": losses,
            "breakeven_trades": breakeven,
            "win_rate": round(
                (wins / total) * 100,
                2,
            ) if total else 0,
            "net_pnl": net_pnl,
            "average_pnl": (
                net_pnl / total
                if total
                else ZERO
            ),
        }

    return result


# =========================================================
# SYMBOL / STRATEGY PERFORMANCE
# =========================================================

def performance_by_field(trades, field):
    groups = defaultdict(list)

    for trade in trades:
        value = getattr(trade, field)

        if not value:
            value = "Unknown"

        groups[str(value)].append(trade)

    result = []

    for name, group in groups.items():
        total = len(group)

        wins = sum(
            1
            for trade in group
            if trade_net_pnl(trade) > ZERO
        )

        losses = sum(
            1
            for trade in group
            if trade_net_pnl(trade) < ZERO
        )

        breakeven = sum(
            1
            for trade in group
            if trade_net_pnl(trade) == ZERO
        )

        net_pnl = sum(
            (
                trade_net_pnl(trade)
                for trade in group
            ),
            ZERO,
        )

        result.append({
            "name": name,
            "trades": total,
            "winning_trades": wins,
            "losing_trades": losses,
            "breakeven_trades": breakeven,
            "win_rate": round(
                (wins / total) * 100,
                2,
            ) if total else 0,
            "net_pnl": net_pnl,
            "average_pnl": (
                net_pnl / total
                if total
                else ZERO
            ),
        })

    return sorted(
        result,
        key=lambda item: item["net_pnl"],
        reverse=True,
    )


# =========================================================
# R MULTIPLE
# =========================================================

def calculate_r_multiple(trade):
    """
    R-multiple based on price risk.

    LONG:
        risk   = entry - stop
        reward = exit - entry

    SHORT:
        risk   = stop - entry
        reward = entry - exit
    """

    if (
        trade.stop_loss is None
        or trade.exit_price is None
    ):
        return None

    entry = decimal(trade.entry_price)
    exit_price = decimal(trade.exit_price)
    stop = decimal(trade.stop_loss)

    if trade.direction == "LONG":
        risk = entry - stop
        reward = exit_price - entry

    else:
        risk = stop - entry
        reward = entry - exit_price

    if risk <= ZERO:
        return None

    return reward / risk


def r_multiple_analysis(trades):
    values = []

    for trade in trades:
        r_multiple = calculate_r_multiple(trade)

        if r_multiple is not None:
            values.append({
                "trade_id": trade.id,
                "symbol": trade.symbol,
                "direction": trade.direction,
                "r": r_multiple,
                "date": trade.entry_time,
            })

    if not values:
        return {
            "average_r": None,
            "largest_r": None,
            "smallest_r": None,
            "trades_with_r": 0,
            "distribution": [],
        }

    r_values = [
        item["r"]
        for item in values
    ]

    return {
        "average_r": (
            sum(r_values, ZERO)
            / len(r_values)
        ),
        "largest_r": max(r_values),
        "smallest_r": min(r_values),
        "trades_with_r": len(r_values),
        "distribution": values,
    }


# =========================================================
# AVERAGE R:R
# =========================================================

def average_rr(trades):
    ratios = []

    for trade in trades:
        if (
            trade.stop_loss is None
            or trade.take_profit is None
        ):
            continue

        entry = decimal(trade.entry_price)
        stop = decimal(trade.stop_loss)
        take_profit = decimal(trade.take_profit)

        if trade.direction == "LONG":
            risk = entry - stop
            reward = take_profit - entry

        else:
            risk = stop - entry
            reward = entry - take_profit

        if risk <= ZERO or reward < ZERO:
            continue

        ratios.append(
            reward / risk
        )

    if not ratios:
        return None

    return (
        sum(ratios, ZERO)
        / len(ratios)
    )


# =========================================================
# WINNING / LOSING STREAKS
# =========================================================

def streaks(trades):
    current_win = 0
    current_loss = 0

    winning_streak = 0
    losing_streak = 0

    for trade in trades:
        pnl = trade_net_pnl(trade)

        if pnl > ZERO:
            current_win += 1
            current_loss = 0

            winning_streak = max(
                winning_streak,
                current_win,
            )

        elif pnl < ZERO:
            current_loss += 1
            current_win = 0

            losing_streak = max(
                losing_streak,
                current_loss,
            )

        else:
            current_win = 0
            current_loss = 0

    return {
        "winning_streak": winning_streak,
        "losing_streak": losing_streak,
    }


# =========================================================
# BEST / WORST TRADING DAY
# =========================================================

def trading_days(trades):
    daily = defaultdict(lambda: ZERO)

    for trade in trades:
        date = trade.entry_time.date()

        daily[date] += trade_net_pnl(trade)

    if not daily:
        return {
            "best_trading_day": None,
            "worst_trading_day": None,
        }

    best = max(
        daily.items(),
        key=lambda item: item[1],
    )

    worst = min(
        daily.items(),
        key=lambda item: item[1],
    )

    return {
        "best_trading_day": {
            "date": best[0],
            "pnl": best[1],
        },
        "worst_trading_day": {
            "date": worst[0],
            "pnl": worst[1],
        },
    }


# =========================================================
# CALENDAR P/L
# =========================================================

def calendar_pnl(trades):
    daily = defaultdict(lambda: ZERO)

    for trade in trades:
        date = trade.entry_time.date()

        daily[date] += trade_net_pnl(trade)

    return [
        {
            "date": date,
            "pnl": pnl,
        }
        for date, pnl in sorted(daily.items())
    ]


# =========================================================
# TRADE FREQUENCY
# =========================================================

def trade_frequency(trades):
    trade_list = list(trades)

    total = len(trade_list)

    if not total:
        return {
            "total_trades": 0,
            "trading_days": 0,
            "average_trades_per_day": 0,
            "trades_per_week": 0,
            "trades_per_month": 0,
        }

    dates = {
        trade.entry_time.date()
        for trade in trade_list
    }

    trading_days_count = len(dates)

    weeks = {
        (
            trade.entry_time.isocalendar().year,
            trade.entry_time.isocalendar().week,
        )
        for trade in trade_list
    }

    months = {
        (
            trade.entry_time.year,
            trade.entry_time.month,
        )
        for trade in trade_list
    }

    return {
        "total_trades": total,
        "trading_days": trading_days_count,
        "average_trades_per_day": round(
            total / trading_days_count,
            2,
        ),
        "trades_per_week": round(
            total / len(weeks),
            2,
        ),
        "trades_per_month": round(
            total / len(months),
            2,
        ),
    }


# =========================================================
# AVERAGE HOLDING TIME
# =========================================================

def holding_time(trades):
    durations = []

    for trade in trades:
        if not trade.exit_time:
            continue

        duration = (
            trade.exit_time
            - trade.entry_time
        )

        durations.append(duration)

    if not durations:
        return {
            "average_seconds": 0,
            "average_minutes": 0,
            "average_hours": 0,
        }

    average = (
        sum(durations, timedelta())
        / len(durations)
    )

    seconds = average.total_seconds()

    return {
        "average_seconds": round(
            seconds,
            2,
        ),
        "average_minutes": round(
            seconds / 60,
            2,
        ),
        "average_hours": round(
            seconds / 3600,
            2,
        ),
    }


# =========================================================
# BEST / WORST SYMBOL
# =========================================================

def best_and_worst_symbol(trades):
    performance = performance_by_field(
        trades,
        "symbol",
    )

    if not performance:
        return {
            "best_performing_symbol": None,
            "worst_performing_symbol": None,
        }

    return {
        "best_performing_symbol": performance[0],
        "worst_performing_symbol": performance[-1],
    }


# =========================================================
# MAIN ANALYTICS BUILDER
# =========================================================

def build_analytics(user):
    trades = get_user_trades(user)

    basic = basic_statistics(trades)

    equity = equity_curve(trades)

    return {
        # Basic statistics
        **basic,

        # Drawdown
        "maximum_drawdown": (
            equity["maximum_drawdown"]
        ),
        "current_drawdown": (
            equity["current_drawdown"]
        ),

        # Equity
        "equity_curve": equity["data"],

        # Time-based P/L
        "daily_pnl": group_pnl(
            trades,
            "daily",
        ),
        "weekly_pnl": group_pnl(
            trades,
            "weekly",
        ),
        "monthly_pnl": group_pnl(
            trades,
            "monthly",
        ),
        "yearly_pnl": group_pnl(
            trades,
            "yearly",
        ),

        # Direction
        "long_vs_short": direction_performance(
            trades
        ),

        # Symbol
        "symbol_performance": (
            performance_by_field(
                trades,
                "symbol",
            )
        ),

        # Strategy / setup
        "strategy_performance": (
            performance_by_field(
                trades,
                "setup",
            )
        ),

        # Risk / reward
        "average_rr": average_rr(
            trades
        ),

        "r_multiple_analysis": (
            r_multiple_analysis(
                trades
            )
        ),

        # Streaks
        **streaks(trades),

        # Best / worst days
        **trading_days(trades),

        # Calendar
        "calendar_pnl": calendar_pnl(
            trades
        ),

        # Frequency
        "trade_frequency": trade_frequency(
            trades
        ),

        # Holding time
        "average_holding_time": holding_time(
            trades
        ),

        # Best / worst symbols
        **best_and_worst_symbol(
            trades
        ),
    }