from services.test_fix_service import TestFixService


def main():
    failing_report = """
## 1. Test Summary

Overall Status: FAIL

Some requirement checks:
- Authentication: PASS
- RBAC: PASS
- Appointment Management: PASS

## 8. Final Testing Decision

FAIL

The project has critical defects.
"""

    warning_report = """
## 8. Final Testing Decision

PASS WITH WARNINGS

Minor improvements remain.
"""

    passing_report = """
## 8. Final Testing Decision

PASS

All required checks passed.
"""

    checks = {
        "fail_detected": (
            TestFixService._extract_status(failing_report)
            == "FAIL"
        ),
        "warnings_detected": (
            TestFixService._extract_status(warning_report)
            == "PASS WITH WARNINGS"
        ),
        "pass_detected": (
            TestFixService._extract_status(passing_report)
            == "PASS"
        ),
    }

    for name, passed in checks.items():
        print(f"{'✅' if passed else '❌'} {name}")

    assert all(checks.values())

    print("\n✅ Phase 12.3 Status Detection Test PASSED")


if __name__ == "__main__":
    main()