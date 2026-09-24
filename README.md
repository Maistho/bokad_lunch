## Lunch menu from Bokad.se

Supported restaurants:
- Stångs Mjärdevi `stangs-mjardevi`

### Weekly Menu
Markdown card with the rest of the weeks menu:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: >
      {% set menu = state_attr('sensor.stangs_mjardevi_dagens_gront',
      'weekly_menu') or [] %}

      {% for item in menu %}

      {% if as_local(as_datetime(item.workday)) >= as_local(today_at("00:00"))
      %}

      #### {{ as_datetime(item.workday).strftime('%A %B %-d') }}

      **{{ state_attr('sensor.stangs_mjardevi_dagens_ratt',
      'weekly_menu')[loop.index-1].name | replace('DAGENS RÄTT: ', '') | title
      }}** _{{ state_attr('sensor.stangs_mjardevi_dagens_ratt',
      'weekly_menu')[loop.index-1].description[0] | capitalize ~
      state_attr('sensor.stangs_mjardevi_dagens_ratt',
      'weekly_menu')[loop.index-1].description[1:] }}_

      **{{ item.name | replace('DAGENS GRÖNT : ', '') | title }}** _{{
      item.description[0] | capitalize ~ item.description[1:] }}_

      {% if not loop.last %}

      ---

      {% endif %}

      {% endif %}

      {% endfor %}
    title: Stångs Mjärdevi
```
