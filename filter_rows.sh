#!/bin/bash
# usage: filt.sh table
t=$1
ROOT=$(pwd); cd "$ROOT/go/Graduate Outcome"
PAT='^(\xef\xbb\xbf)?(10006840|10007786|10007788|10007814|10007143|10007790|10007792|10007794|10003270|10003645|10007795|10006842|10004063|10007798|10007799|10007154|10007774|10007775|10005343|10007157|10007158|10007784|10007163|10007167|10042500),'
for f in $(unzip -Z1 table-$t.zip); do
  y=$(echo $f | sed -E 's/.*-([0-9]{4}-[0-9]{2})\.csv/\1/')
  ( unzip -p table-$t.zip $f | tr -d '\r' | awk -v pat="$PAT" 'BEGIN{h=0} { if(!h){ if($0 ~ /^UKPRN,/ || $0 ~ /^\xef\xbb\xbfUKPRN,/){print; h=1} } else if ($0 ~ pat) print }' ) > "$ROOT/flt/table-$t-$y.csv"
done
echo done $t
