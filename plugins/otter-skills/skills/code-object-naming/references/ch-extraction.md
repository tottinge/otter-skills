# Digest: Extraction and Naming (ch: extraction)

> "You have two important decisions to make: 1) what to name, and 2) what to
> call it." — Eddie Bush

Extraction and naming are two sides of the same coin. Every extraction
requires a new name. Every good name suggests what might be worth extracting.

## Paragraph comments → function names

Paragraph comments inside a function are the code announcing what it's about
to do:

```python
def export(output_filename, data_to_write):
    # Ensure the data is not empty
    ...
    # Ensure the directory exists
    ...
    # Write data as CSV
    ...
```

These markers suggest concepts to investigate. Check whether an existing owner,
a named expression, or a function would express the knowledge better. Extract only
when the boundary improves understanding and changeability; remove a comment only
when its useful meaning is carried by the code. Preserve otherwise inexpressible
rationale. The following is one possible improvement, not a required shape:

```python
def export(output_filename: str, data_to_write: DataSet):
    if data_to_write.is_empty():
        raise NoDataToWriteError()
    with open_output(output_filename) as output_file:
        write_csv(output_file, data_to_write)
```

## Complex boolean → predicate function

A long compound condition signals an extraction:

```python
# Hard to parse inline
if (order.total > 1000 and customer.membership_level == 'premium' and
    customer.account_age_months > 12 and ...):
    ...

# Extract to a named predicate
if is_eligible_for_express_processing(order, customer, inventory):
    ...
```

Benefits of extraction over an explanatory variable:
- **Browseability**: callers can skip the detail; readers scan without reading
- **Testability**: the predicate can be unit-tested independently
- **Reuse**: the condition can be called from multiple sites
- **Single Point of Truth**: the boolean logic lives in one place

When the expression is only used once and the function is short, an
explanatory variable is an acceptable lighter alternative:
```python
eligible_for_express = order.total > 1000 and ...
if eligible_for_express:
    ...
```
The variable approach loses browseability and testability but gains
debuggability and is easier to extract later.

## Class naming difficulty → split signal

> When you can't name a class because it seems to do multiple things,
> you're probably looking at multiple classes sharing one definition.

```python
# Hard to name — it does: validation, pricing, payment, inventory, shipping, loyalty
class CustomerOrderProcessor:
    def validate_order(self, order): ...
    def calculate_pricing(self, order, customer): ...
    def process_payment(self, order): ...
    def update_inventory(self, order): ...
    def schedule_shipment(self, order): ...
    def award_loyalty_points(self, customer, order): ...
```

When naming is difficult, investigate whether independent concepts are combined.
The word "and" alone is not evidence for splitting: a coherent owner may coordinate
several operations under one invariant or lifecycle. Use the class-boundary
guidance in `representation-refactor-review` to inspect construction, shared rules,
and interactions before recommending a split.

## Explanatory variable as a stepping stone

Isolate a complex expression in a variable first, then extract the variable
to a function. This two-step makes extraction safer and easier to verify.

## Naming as vocabulary building

> Extraction is not just moving text — it's building vocabulary.

A useful extracted function names a concept. A codebase with good function
names is **browseable**: readers can scan function calls without reading
implementations, find what they need, and change it safely.

## Extraction moments (decision table)

| Signal in code | Candidate to investigate |
|---|---|
| Inline comment describes a block | Extract block to function; comment → name |
| Long boolean condition | Extract to `is_X()` / `can_X()` predicate |
| Complex expression assigned to variable | Extract variable → then function |
| Class is hard to name | Identify multiple responsibilities; split class |
| `as_X()` conversion on a host object | Extract a whole value object type |
| Same expression duplicated | Extract to a Single Point of Truth function |
| Name is clear inside module, confusing outside | Add import alias; or rename class |

These candidates are not prescriptions. Compare local vocabulary and existing
owners, preserve behavior, and apply the improvement test across the peer virtues.
Reject or shrink an extraction that adds indirection without improving ownership
or the work of understanding and changing the code.
