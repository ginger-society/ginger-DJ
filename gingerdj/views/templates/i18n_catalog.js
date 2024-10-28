{% autoescape off %}
'use strict';
{
  const globals = this;
  const gingerdj = globals.gingerdj || (globals.gingerdj = {});

  {% if plural %}
  gingerdj.pluralidx = function(n) {
    const v = {{ plural }};
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  {% else %}
  gingerdj.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  {% endif %}

  /* gettext library */

  gingerdj.catalog = gingerdj.catalog || {};
  {% if catalog_str %}
  const newcatalog = {{ catalog_str }};
  for (const key in newcatalog) {
    gingerdj.catalog[key] = newcatalog[key];
  }
  {% endif %}

  if (!gingerdj.jsi18n_initialized) {
    gingerdj.gettext = function(msgid) {
      const value = gingerdj.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    gingerdj.ngettext = function(singular, plural, count) {
      const value = gingerdj.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[gingerdj.pluralidx(count)] : value;
      }
    };

    gingerdj.gettext_noop = function(msgid) { return msgid; };

    gingerdj.pgettext = function(context, msgid) {
      let value = gingerdj.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    gingerdj.npgettext = function(context, singular, plural, count) {
      let value = gingerdj.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = gingerdj.ngettext(singular, plural, count);
      }
      return value;
    };

    gingerdj.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    gingerdj.formats = {{ formats_str }};

    gingerdj.get_format = function(format_type) {
      const value = gingerdj.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = gingerdj.pluralidx;
    globals.gettext = gingerdj.gettext;
    globals.ngettext = gingerdj.ngettext;
    globals.gettext_noop = gingerdj.gettext_noop;
    globals.pgettext = gingerdj.pgettext;
    globals.npgettext = gingerdj.npgettext;
    globals.interpolate = gingerdj.interpolate;
    globals.get_format = gingerdj.get_format;

    gingerdj.jsi18n_initialized = true;
  }
};
{% endautoescape %}
