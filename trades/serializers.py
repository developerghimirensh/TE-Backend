from rest_framework import serializers

from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade

        fields = [
            "id",
            "user",
            "entry_time",
            "exit_time",
            "symbol",
            "direction",
            "lots",
            "entry_price",
            "take_profit",
            "stop_loss",
            "exit_price",
            "pnl",
            "fees",
            "setup",
            "lesson",
            "score",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]

    def validate_score(self, value):
        if value is not None and not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Score must be between 1 and 10."
            )

        return value

    def validate_lots(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Lots must be greater than 0."
            )

        return value

    def validate_entry_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Entry price must be greater than 0."
            )

        return value

    def validate_take_profit(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Take profit must be greater than 0."
            )

        return value

    def validate_stop_loss(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Stop loss must be greater than 0."
            )

        return value

    def validate_exit_price(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Exit price must be greater than 0."
            )

        return value

    def validate_fees(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Fees cannot be negative."
            )

        return value

    def validate(self, data):
        entry_time = data.get("entry_time")
        exit_time = data.get("exit_time")

        entry_price = data.get("entry_price")
        take_profit = data.get("take_profit")
        stop_loss = data.get("stop_loss")

        direction = data.get("direction")

        # Exit time validation
        if (
            exit_time
            and entry_time
            and exit_time < entry_time
        ):
            raise serializers.ValidationError({
                "exit_time": (
                    "Exit time cannot be before entry time."
                )
            })

        # TP / SL validation
        if entry_price and direction == "LONG":
            if take_profit is not None and take_profit <= entry_price:
                raise serializers.ValidationError({
                    "take_profit": (
                        "For a LONG trade, take profit "
                        "must be above the entry price."
                    )
                })

            if stop_loss is not None and stop_loss >= entry_price:
                raise serializers.ValidationError({
                    "stop_loss": (
                        "For a LONG trade, stop loss "
                        "must be below the entry price."
                    )
                })

        if entry_price and direction == "SHORT":
            if take_profit is not None and take_profit >= entry_price:
                raise serializers.ValidationError({
                    "take_profit": (
                        "For a SHORT trade, take profit "
                        "must be below the entry price."
                    )
                })

            if stop_loss is not None and stop_loss <= entry_price:
                raise serializers.ValidationError({
                    "stop_loss": (
                        "For a SHORT trade, stop loss "
                        "must be above the entry price."
                    )
                })

        return data