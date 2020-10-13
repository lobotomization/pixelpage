#!/bin/bash
VER=$1

sed -i "1s/^/from . import "$VER"\n/" __init__.py


ROUTES=(`grep route "$VER.py" | cut -d '"' -f 2`)
for route in "${ROUTES[@]}"
do
	FUNC=`grep 'route("'"$route"'"' "$VER.py" -A 1 | grep def | cut -d ' ' -f 2 | tr -d '():'`
	LINENUM=`grep -n add_url_rule __init__.py | tail -n 1 | cut -d ':' -f 1`
	(( LINENUM++ ))
	sed -i $LINENUM"i app.add_url_rule(\"$route\", view_func=$VER.$FUNC)" __init__.py
	echo "Route "$route" linked to view function "$FUNC" on line "$LINENUM" of __init__.py."
done
