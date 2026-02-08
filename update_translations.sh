#!/bin/bash
set -e

DOMAIN="bigcontrolcenter"
POT_FILE="bigcontrolcenter/locale/$DOMAIN.pot"

echo "Generating file list..."
# Find all Python files
find bigcontrolcenter -name "*.py" | sort >files_to_translate.txt

echo "Extracting strings to $POT_FILE..."
# Extract strings
# --no-location to avoid noise in diffs if lines change often? No, usually we want locations.
# But verify if content has location. Yes it does.
xgettext --files-from=files_to_translate.txt \
	--language=Python \
	--keyword=_ \
	--keyword=N_ \
	--output="$POT_FILE" \
	--from-code=UTF-8 \
	--package-name="BigControlCenter" \
	--package-version="1.0" \
	--copyright-holder="BigLinux Team" \
	--add-comments=Note:

echo "Generating Shell file list..."
find bigcontrolcenter -name "*.sh" -o -name "*.sh.htm" | sort >shell_files_to_translate.txt

echo "Extracting Shell strings to $POT_FILE..."
# Extract Shell strings and join
xgettext --files-from=shell_files_to_translate.txt \
	--language=Shell \
	--keyword=$ \
	--join-existing \
	--output="$POT_FILE" \
	--from-code=UTF-8 \
	--add-comments=Note:

echo "Updating PO files..."
# Merge with existing PO files
for po_file in bigcontrolcenter/locale/*.po; do
	echo "Updating $po_file..."
	msgmerge --update --backup=none "$po_file" "$POT_FILE"
	# Remove obsolete strings
	msgattrib --no-obsolete -o "$po_file" "$po_file"
done

# Cleanup
rm files_to_translate.txt shell_files_to_translate.txt

echo "Done."
