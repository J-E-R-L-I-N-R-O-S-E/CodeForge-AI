from services.test_fix_service import TestFixService


def main():
    malformed_output = """
### File: frontend/src/pages/Dashboard.js
import React from "react";

function Dashboard() {
    return <div>Dashboard</div>;
}

FILE_CONTENTS_START
export default Dashboard;
FILE_CONTENTS_END
"""

    normalized = TestFixService._normalize_developer_output(
        malformed_output
    )

    print("Normalized output:")
    print(normalized)
    print()

    assert "### File: frontend/src/pages/Dashboard.js" in normalized
    assert normalized.count("FILE_CONTENTS_START") == 1
    assert normalized.count("FILE_CONTENTS_END") == 1

    # The content that appeared before START should now
    # be inside the file-content section.
    assert 'import React from "react";' in normalized
    assert 'function Dashboard()' in normalized
    assert 'export default Dashboard;' in normalized

    # The malformed ordering must be gone.
    header_end = normalized.index(
        "### File: frontend/src/pages/Dashboard.js"
    )

    marker_start = normalized.index(
        "FILE_CONTENTS_START"
    )

    assert header_end < marker_start

    print("✅ malformed_output normalized")
    print("✅ file markers preserved")
    print("✅ source moved inside content section")
    print()
    print("✅ Developer Output Normalization Test PASSED")


if __name__ == "__main__":
    main()