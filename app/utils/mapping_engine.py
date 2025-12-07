import json
from copy import deepcopy
from typing import Any, Optional

from jsonpath_ng import parse

from sqlalchemy.orm import Session

from app.models.mapping import MappingProfile, MappingRule, MappingAction


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def json_get(root: Any, path: str) -> Any:
    """Extract value(s) using JSONPath."""
    expr = parse(path)
    matches = expr.find(root)
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0].value
    return [m.value for m in matches]


def json_set(root: Any, path: str, value: Any):
    """Set or overwrite value(s) using JSONPath."""
    expr = parse(path)
    matches = expr.find(root)

    if matches:
        # Overwrite existing nodes
        for match in matches:
            full_path = match.full_path
            full_path.update(root, value)
    else:
        # Create missing nodes if path doesn't exist
        # jsonpath-ng does not auto-create. So we only assign at root level.
        # If deep path creation is needed, implement manually.
        root[path.replace("$.","")] = value

    return root


# ---------------------------------------------------------
# Transformation evaluator
# ---------------------------------------------------------

def apply_transform(value: Any, expr: Optional[str]) -> Any:
    """Optional Python expression to transform the value."""
    if not expr:
        return value
    try:
        local = {"value": value}
        return eval(expr, {}, local)
    except Exception:
        return value


# ---------------------------------------------------------
# Main executor
# ---------------------------------------------------------

def apply_mapping_profile(profile_id: int, source_json: Any, db: Session) -> Any:
    """Convert JSON using mapping rules."""
    profile = db.query(MappingProfile).get(profile_id)
    if not profile:
        raise ValueError("MappingProfile not found")

    rules = (
        db.query(MappingRule)
        .filter(MappingRule.profile_id == profile_id)
        .order_by(MappingRule.order_index.asc())
        .all()
    )

    target = {}

    for rule in rules:
        action = rule.action

        # MAP
        if action == MappingAction.MAP:
            src_val = json_get(source_json, rule.source_json_path)
            if src_val is None:
                continue
            src_val = apply_transform(src_val, rule.transform_expr)
            json_set(target, rule.target_json_path, src_val)

        # IGNORE
        elif action == MappingAction.IGNORE:
            continue

        # DEFAULT
        elif action == MappingAction.DEFAULT:
            src_val = json_get(source_json, rule.source_json_path)
            if src_val is None:
                src_val = rule.default_value
            src_val = apply_transform(src_val, rule.transform_expr)
            json_set(target, rule.target_json_path, src_val)

        # ADD
        elif action == MappingAction.ADD:
            val = apply_transform(rule.default_value, rule.transform_expr)
            json_set(target, rule.target_json_path, val)

    return target
