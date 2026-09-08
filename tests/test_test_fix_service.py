from pathlib import Path

from services.test_fix_service import TestFixService


class FakeTestingService:
    def __init__(self):
        self.analyze_calls = 0
        self.inspect_calls = 0

    def analyze_project(
        self,
        project_path,
        confirmed_requirements,
        architecture,
        project_idea="",
    ):
        self.analyze_calls += 1

        if self.analyze_calls == 1:
            return """
        ## 8. Final Testing Decision
        FAIL
        """

        return """
        ## 8. Final Testing Decision

        PASS
        """

    def inspect_project(self, project_path):
        self.inspect_calls += 1

        return {
            "project_structure": "app.py",
            "project_code": "print('test')",
        }


class FakeDeveloperAgent:
    def __init__(self):
        self.generate_calls = 0
        self.received_prompt = None
        self.received_provider = None

    def generate(self, prompt, preferred_provider=None):
        self.generate_calls += 1
        self.received_prompt = prompt
        self.received_provider = preferred_provider

        return """
### File: app.py
FILE_CONTENTS_START
print("fixed")
FILE_CONTENTS_END
"""


class FakeCodeGenerator:
    def __init__(self):
        self.write_calls = 0

    def write_project(self, project_name, developer_output):
        self.write_calls += 1
        return ["app.py"]


def main():
    project_path = Path("outputs/test-fix-demo")
    project_path.mkdir(parents=True, exist_ok=True)

    testing_service = FakeTestingService()
    developer_agent = FakeDeveloperAgent()
    code_generator = FakeCodeGenerator()

    service = TestFixService(
        testing_service=testing_service,
        developer_agent=developer_agent,
        code_generator=code_generator,
    )

    result = service.run(
        project_path=project_path,
        confirmed_requirements="Admin can manage appointments.",
        architecture="React, Node.js, PostgreSQL, Prisma.",
        project_idea="Hospital Management System",
        max_retries=3,
    )

    checks = {
        "initial_test_called": testing_service.analyze_calls >= 1,
        "retest_called": testing_service.analyze_calls == 2,
        "inspection_called": testing_service.inspect_calls == 1,
        "developer_called": developer_agent.generate_calls == 1,
        "preferred_provider_passed": (
                    developer_agent.received_provider == "groq"
        ),
        "code_generator_called": code_generator.write_calls == 1,
        "final_status_pass": result["final_status"] == "PASS",
        "fix_recorded": len(result["fixes_applied"]) == 1,
        "retry_count": result["attempts"] == 1,
    }

    for name, passed in checks.items():
        print(f"{'✅' if passed else '❌'} {name}")

    assert all(checks.values())

    print("\n✅ Phase 12.2 Test ↔ Fix Service Wiring PASSED")


if __name__ == "__main__":
    main()