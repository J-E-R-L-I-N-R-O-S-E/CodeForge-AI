from services.test_fix_service import TestFixService


def main():
    valid_output = """
### File: frontend/src/pages/Dashboard.js
FILE_CONTENTS_START
import React from "react";

function Dashboard() {
    return <div>Dashboard</div>;
}

export default Dashboard;
FILE_CONTENTS_END
"""

    invalid_output = """
### File: frontend/src/pages/Dashboard.js
import React from "react";
FILE_CONTENTS_START
export default Dashboard;
FILE_CONTENTS_END
"""

    malformed_path = """
### File: frontend/src/pages/Dashboard.js
some unexpected content
FILE_CONTENTS_START
console.log("test");
FILE_CONTENTS_END
"""

    # Valid output must pass.
    TestFixService._validate_developer_output(
        valid_output
    )

    # Invalid output must fail.
    try:
        TestFixService._validate_developer_output(
            invalid_output
        )
        invalid_passed = True
    except ValueError:
        invalid_passed = False

    try:
        TestFixService._validate_developer_output(
            malformed_path
        )
        malformed_passed = True
    except ValueError:
        malformed_passed = False

    print(
        f"{'✅' if not invalid_passed else '❌'} invalid_format_rejected"
    )

    print(
        f"{'✅' if not malformed_passed else '❌'} malformed_path_rejected"
    )

    print("✅ valid_format_accepted")

    assert not invalid_passed
    assert not malformed_passed

    print(
        "\n✅ Developer Output Validation Test PASSED"
    )


if __name__ == "__main__":
    main()