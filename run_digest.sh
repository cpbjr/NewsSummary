#!/bin/bash
# DST-aware digest runner — checks Mountain Time before running aggregator

MT_HOUR=$(TZ=America/Denver date +%-H)

case $MT_HOUR in
  6)  DIGEST="morning" ;;
  12) DIGEST="noon" ;;
  18) DIGEST="evening" ;;
  *)  exit 0 ;;
esac

cd /var/www/newssummary
echo "[$(date)] Running $DIGEST digest (MT hour: $MT_HOUR)" >> /var/log/newssummary_cron.log
./venv/bin/python src/aggregator.py $DIGEST >> /var/log/newssummary_cron.log 2>&1
