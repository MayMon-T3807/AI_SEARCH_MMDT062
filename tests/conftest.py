import os
import pytest

def pytest_configure(config):
    # Dictionary mapping nodeid to test details
    config._test_results = {}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    # We retrieve markers
    weight_marker = item.get_closest_marker('weight')
    number_marker = item.get_closest_marker('number')
    
    weight = weight_marker.args[0] if weight_marker else 0
    number = number_marker.args[0] if number_marker else ""
    
    description = item.obj.__doc__ if item.obj and item.obj.__doc__ else item.name
    if description:
        # Get first line and clean up
        description = description.split('\n')[0].strip()
        
    if rep.when == 'call':
        if rep.passed:
            status = 'PASS'
        elif rep.failed:
            status = 'FAIL'
        else:
            status = 'SKIP'
        
        earned = weight if status == 'PASS' else 0
        if hasattr(item, '_earned_points'):
            earned = item._earned_points
        
        item.config._test_results[item.nodeid] = {
            'number': number,
            'weight': weight,
            'description': description,
            'status': status,
            'earned': earned
        }
    elif rep.when == 'setup' and rep.failed:
        earned = 0
        if hasattr(item, '_earned_points'):
            earned = item._earned_points
        item.config._test_results[item.nodeid] = {
            'number': number,
            'weight': weight,
            'description': description,
            'status': 'FAIL',
            'earned': earned
        }

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    results = getattr(config, '_test_results', {})
    if not results:
        return
        
    cat_names = {
        "1": "Implementation Tasks",
        "2": "report.md Completion Tasks"
    }
    
    # Group tests
    grouped = {}
    for nodeid, res in results.items():
        num = res['number']
        parts = num.split('.')
        prefix = parts[0] if parts else ""
        
        if prefix not in cat_names:
            cat_name = "Other Tasks"
        else:
            cat_name = cat_names[prefix]
            
        if cat_name not in grouped:
            grouped[cat_name] = []
        grouped[cat_name].append(res)
        
    cat_order = {
        "Implementation Tasks": 1,
        "report.md Completion Tasks": 2
    }
    
    sorted_categories = sorted(grouped.keys(), key=lambda c: cat_order.get(c, 99))
    
    lines = []
    lines.append("======================================================================")
    lines.append("                    AUTOGRADING SCORECARD")
    lines.append("======================================================================")
    lines.append(f"{'Task Name':<46}{'Max Marks':<11}{'Earned':<11}{'Status':<12}".rstrip())
    lines.append("----------------------------------------------------------------------")
    
    total_max = 0
    total_earned = 0
    
    for cat in sorted_categories:
        cat_tests = grouped[cat]
        # Sort tests by their number marker
        def test_sort_key(res):
            num = res['number']
            parts = num.split('.')
            try:
                return [int(p) for p in parts if p.isdigit()]
            except ValueError:
                return [999]
        cat_tests = sorted(cat_tests, key=test_sort_key)
        
        cat_max = sum(t['weight'] for t in cat_tests)
        cat_earned = sum(t['earned'] for t in cat_tests)
        
        total_max += cat_max
        total_earned += cat_earned
        
        lines.append(f"[{cat}] (Max: {cat_max} marks)")
        
        for t in cat_tests:
            desc = t['description'] or ""
            if len(desc) > 42:
                desc = desc[:42] + "..."
            
            line = f"{desc:<46}{t['weight']:<11}{t['earned']:<11}{t['status']:<12}".rstrip()
            lines.append(line)
            
    import datetime
    due_date = datetime.datetime(2026, 9, 13, 23, 59, 59)
    
    grading_time_env = os.environ.get("GRADING_TIME")
    if grading_time_env:
        try:
            current_time = datetime.datetime.fromisoformat(grading_time_env)
        except Exception:
            current_time = datetime.datetime.now()
    else:
        current_time = datetime.datetime.now()
        
    days_late = 0
    if current_time > due_date:
        diff = current_time - due_date
        days_late = diff.days
        if diff.total_seconds() > days_late * 86400:
            days_late += 1
            
    penalty = days_late * 10
    final_score = max(0, total_earned - penalty)
    
    if days_late > 0:
        lines.append(f"Submission Status: LATE by {days_late} day(s)")
        lines.append(f"Late Penalty:      -{penalty} marks (-10 marks/day)")
    else:
        lines.append("Submission Status: ON TIME")
        
    lines.append(f"Final Result: TOTAL SCORE: {final_score} / {total_max} marks")
    lines.append("======================================================================")
    
    scorecard_text = "\n".join(lines)
    
    # Write to terminal
    terminalreporter._tw.line()
    for line in lines:
        terminalreporter._tw.line(line)
    terminalreporter._tw.line()
    
    # Write to GITHUB_STEP_SUMMARY if available
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write("### Autograding Scorecard\n\n")
                f.write("```text\n")
                f.write(scorecard_text + "\n")
                f.write("```\n")
        except Exception as e:
            # Avoid crashing the test runner if writing summary fails
            pass
