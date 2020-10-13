#!/bin/bash
VER=$1

if grep -q 'import '$VER __init__.py
then
	echo "$VER.py already imported into __init__.py"
else
	sed -i "1s/^/from . import "$VER"\n/" __init__.py
	echo "$VER.py imported into __init__.py"
fi

ROUTES=(`grep route "$VER.py" | cut -d '"' -f 2`)
for route in "${ROUTES[@]}"
do
	FUNC=`grep 'route("'"$route"'"' "$VER.py" -A 1 | grep def | cut -d ' ' -f 2 | tr -d '():'`
	LINENUM=`grep -n add_url_rule __init__.py | tail -n 1 | cut -d ':' -f 1`
	(( LINENUM++ ))
	if grep -q 'app.add_url_rule("'$route'"' __init__.py 
	then
		echo "Route "$route" already linked to view function in __init__.py."
	else
		sed -i $LINENUM"i app.add_url_rule(\"$route\", view_func=$VER.$FUNC)" __init__.py
		echo "Route "$route" linked to view function "$FUNC" on line "$LINENUM" of __init__.py."

	fi
done
