{% test review_counts_make_sense(model, column_name) %}

select
    {{ column_name }}
from {{ model }}
where {{ column_name }} > 50000000

{% endtest %}
