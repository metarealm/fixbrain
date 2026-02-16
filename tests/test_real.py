#!/usr/bin/env python3
"""
Real Phase 1 test using actual appliance problem images.
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.core.pipeline import run_analysis_pipeline


# Test scenarios with real images
TEST_CASES = [
    {
        "image": "data/images_phase1_seed/2026-02-15-16-26-49-wm-standing-water.png",
        "appliance": "washing machine",
        "problem": "Water won't drain, standing water visible at bottom",
        "task_id": "test_wm_standing_water"
    },
    {
        "image": "data/images_phase1_seed/2026-02-15-16-26-49-wm-drain-pump-clog-closeup.png",
        "appliance": "washing machine",
        "problem": "Drain pump making loud grinding noise, not pumping water",
        "task_id": "test_wm_pump_clog"
    },
    {
        "image": "data/images_phase1_seed/2026-02-15-16-26-49-dishwasher-spray-arm-issue.png",
        "appliance": "dishwasher",
        "problem": "Spray arm not rotating, dishes not getting clean",
        "task_id": "test_dishwasher_spray"
    },
    {
        "image": "data/images_phase1_seed/2026-02-15-16-26-49-fridge-frost-cooling-issue.png",
        "appliance": "refrigerator",
        "problem": "Excessive frost buildup, not cooling properly",
        "task_id": "test_fridge_frost"
    },
    {
        "image": "data/images_phase1_seed/2026-02-15-16-26-49-control-board-burn-mark.png",
        "appliance": "washing machine",
        "problem": "Control board has visible burn marks, machine won't start",
        "task_id": "test_control_board_burn"
    }
]


def run_test(test_case):
    """Run a single test case."""
    print("\n" + "=" * 70)
    print(f"TEST: {test_case['appliance'].upper()} - {test_case['problem']}")
    print("=" * 70)
    print(f"Image: {test_case['image']}")

    # Load image
    with open(test_case['image'], 'rb') as f:
        image_bytes = f.read()

    # Run pipeline
    result = run_analysis_pipeline(
        task_id=test_case['task_id'],
        appliance_type=test_case['appliance'],
        problem_description=test_case['problem'],
        image_bytes=image_bytes
    )

    llm = result['llm_result']

    # Display results
    print(f"\n🎯 DECISION: {llm['decision'].upper()}")
    print(f"💡 RATIONALE: {llm['rationale']}")

    print(f"\n🔍 ROOT CAUSES:")
    for i, cause in enumerate(llm.get('root_causes', []), 1):
        print(f"  {i}. {cause['name']} ({cause['likelihood']:.0%} likelihood)")
        for ev in cause.get('evidence', []):
            print(f"     • {ev}")

    if llm.get('repair'):
        repair = llm['repair']
        print(f"\n🔧 REPAIR PLAN:")
        print(f"  Difficulty: {repair['difficulty']}/5")
        print(f"  Time: {repair['estimated_time_minutes']} min")
        print(f"  Tools: {', '.join(repair['tools'])}")
        print(f"  Parts needed: {len(repair['parts'])}")
        print(f"  Steps: {len(repair['steps'])}")

    print(f"\n✅ Test passed - valid JSON response received")
    return True


def main():
    print("\n🤖 FixBrain Phase 1 - Real Image Test Suite")
    print("=" * 70)

    passed = 0
    failed = 0

    for test_case in TEST_CASES:
        try:
            if run_test(test_case):
                passed += 1
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
