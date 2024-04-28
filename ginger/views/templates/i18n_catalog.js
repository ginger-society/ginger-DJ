{% autoescape off %}
'use strict';
{
  const globals = this;
  const ginger = globals.ginger || (globals.ginger = {});

  {% if plural %}
  ginger.pluralidx = function(n) {
    const v = {{ plural }};
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  {% else %}
  ginger.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  {% endif %}

  /* gettext library */

  ginger.catalog = ginger.catalog || {};
  {% if catalog_str %}
  const newcatalog = {{ catalog_str }};
  for (const key in newcatalog) {
    ginger.catalog[key] = newcatalog[key];
  }
  {% endif %}

  if (!ginger.jsi18n_initialized) {
    ginger.gettext = function(msgid) {
      const value = ginger.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    ginger.ngettext = function(singular, plural, count) {
      const value = ginger.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[ginger.pluralidx(count)] : value;
      }
    };

    ginger.gettext_noop = function(msgid) { return msgid; };

    ginger.pgettext = function(context, msgid) {
      let value = ginger.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    ginger.npgettext = function(context, singular, plural, count) {
      let value = ginger.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = ginger.ngettext(singular, plural, count);
      }
      return value;
    };

    ginger.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    ginger.formats = {{ formats_str }};

    ginger.get_format = function(format_type) {
      const value = ginger.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = ginger.pluralidx;
    globals.gettext = ginger.gettext;
    globals.ngettext = ginger.ngettext;
    globals.gettext_noop = ginger.gettext_noop;
    globals.pgettext = ginger.pgettext;
    globals.npgettext = ginger.npgettext;
    globals.interpolate = ginger.interpolate;
    globals.get_format = ginger.get_format;

    ginger.jsi18n_initialized = true;
  }
};
{% endautoescape %}
