#! /bin/sh

I18NDOMAIN="collective.embedly"
BASE_DIRECTORY="collective/embedly"
I18NDUDE="bin/i18ndude"

# Synchronise the templates and scripts with the .pot.
${I18NDUDE} rebuild-pot --pot ${BASE_DIRECTORY}/locales/${I18NDOMAIN}.pot \
    --merge ${BASE_DIRECTORY}/locales/manual.pot \
    --exclude="index.html" \
    --create ${I18NDOMAIN} \
    ${BASE_DIRECTORY}

# Synchronise the resulting .pot with all .po files
for po in ${BASE_DIRECTORY}/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    ${I18NDUDE} sync --pot ${BASE_DIRECTORY}/locales/${I18NDOMAIN}.pot $po
done

# Report of errors and suspect untranslated messages
${I18NDUDE} find-untranslated -n ${BASE_DIRECTORY}
