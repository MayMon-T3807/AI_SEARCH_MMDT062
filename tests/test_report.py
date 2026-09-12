import os
import re
import pytest

# Resolve the report path.
REPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report.md'))

def get_report_content():
    if not os.path.exists(REPORT_PATH):
        raise AssertionError(f"report.md was not found at {REPORT_PATH}")
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def get_section_discussion_answer(question_keyword, content):
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if question_keyword in line and '**' in line:
            answer_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                # Stop if we hit a new list item, header, or divider
                if next_line.startswith('-') or next_line.startswith('##') or next_line.startswith('---'):
                    break
                if next_line:
                    answer_lines.append(next_line)
            return '\n'.join(answer_lines)
    return None

@pytest.mark.weight(5)
@pytest.mark.number("2.1")
def test_student_information():
    """report.md: Student Information check"""
    content = get_report_content()
    name_match = re.search(r'-\s*\*\*Name:\*\*\s*(.*)', content)
    mmdt_id_match = re.search(r'-\s*\*\*MMDT ID:\*\*\s*(.*)', content)
    
    assert name_match is not None, "Name field not found under Student Information"
    assert mmdt_id_match is not None, "MMDT ID field not found under Student Information"
    
    name = name_match.group(1).strip()
    mmdt_id = mmdt_id_match.group(1).strip()
    
    assert name and name != "[Write your Name here]", "Student Name must be filled out"
    assert not (name.startswith("[") and name.endswith("]")), "Student Name cannot contain placeholder text"
    
    assert mmdt_id and mmdt_id != "[Write your MMDT ID here]", "MMDT ID must be filled out"
    assert not (mmdt_id.startswith("[") and mmdt_id.endswith("]")), "MMDT ID cannot contain placeholder text"

@pytest.mark.weight(5)
@pytest.mark.number("2.2")
def test_selected_city_region():
    """report.md: Selected Region check"""
    content = get_report_content()
    region_match = re.search(r'-\s*\*\*Selected Region:\*\*\s*(.*)', content)
    assert region_match is not None, "Selected Region field not found under Task 1"
    
    region = region_match.group(1).strip()
    assert region and not region.startswith("[Choose one:"), "Selected Region must not be empty or the placeholder template"
    assert not (region.startswith("[") and region.endswith("]")), "Selected Region cannot contain placeholder text"
    
    valid_regions = ["Myanmar", "Thailand"]
    matched = any(vr.lower() == region.lower() for vr in valid_regions)
    assert matched, f"Selected Region '{region}' is not one of the valid geographic regions (Myanmar or Thailand)"

@pytest.mark.weight(5)
@pytest.mark.number("2.3")
def test_map_graph_configuration():
    """report.md: Map Graph Configuration check"""
    content = get_report_content()
    cities_match = re.search(r'-\s*\*\*Total Cities Configured:\*\*\s*(.*)', content)
    edges_match = re.search(r'-\s*\*\*Total Connection Edges:\*\*\s*(.*)', content)
    connected_match = re.search(r'-\s*\*\*Graph Fully Connected:\*\*\s*(.*)', content)
    
    assert cities_match is not None, "Total Cities Configured field not found"
    assert edges_match is not None, "Total Connection Edges field not found"
    assert connected_match is not None, "Graph Fully Connected field not found"
    
    cities_str = cities_match.group(1).strip()
    cities_val_match = re.search(r'\d+', cities_str)
    assert cities_val_match is not None, "Total Cities Configured must contain a numeric value"
    num_cities = int(cities_val_match.group(0))
    assert num_cities >= 20, f"You must configure at least 20 cities (currently: {num_cities})"
    
    edges_str = edges_match.group(1).strip()
    edges_val_match = re.search(r'\d+', edges_str)
    assert edges_val_match is not None, "Total Connection Edges must contain a numeric value"
    num_edges = int(edges_val_match.group(0))
    assert num_edges > 0, "Total Connection Edges must be greater than 0"
    
    connected = connected_match.group(1).strip().lower()
    assert "yes" in connected or "no" in connected, "Graph Fully Connected must be answered with 'Yes' or 'No'"

@pytest.mark.weight(5)
@pytest.mark.number("2.4")
def test_local_verification_checked():
    """report.md: Search Verification checklist"""
    content = get_report_content()
    checked_algs = re.findall(r'-\s*\[[xX]\]\s*(.*)', content)
    assert len(checked_algs) > 0, "No algorithms were checked off as verified on your local development server (marked with [x])"

@pytest.mark.weight(5)
@pytest.mark.number("2.5")
def test_deployment_information():
    """report.md: Live Deployment Details check"""
    content = get_report_content()
    platform_match = re.search(r'-\s*\*\*Deployment Platform:\*\*\s*(.*)', content)
    url_match = re.search(r'-\s*\*\*Live Deployment URL:\*\*\s*(.*)', content)
    video_match = re.search(r'-\s*\*\*Video Presentation Link:\*\*\s*(.*)', content)
    
    assert platform_match is not None, "Deployment Platform field not found"
    assert url_match is not None, "Live Deployment URL field not found"
    assert video_match is not None, "Video Presentation Link field not found"
    
    platform = platform_match.group(1).strip()
    url = url_match.group(1).strip()
    video_link = video_match.group(1).strip()
    
    assert platform and not platform.startswith("["), "Deployment Platform must be completed and cannot be placeholder"
    assert url and not url.startswith("["), "Live Deployment URL must be completed and cannot be placeholder"
    assert url.startswith("http://") or url.startswith("https://"), "Live Deployment URL must be a valid absolute HTTP/HTTPS URL"
    assert video_link and not video_link.startswith("["), "Video Presentation Link must be completed and cannot be placeholder"
    assert video_link.startswith("http://") or video_link.startswith("https://"), "Video Presentation Link must be a valid absolute HTTP/HTTPS URL"

@pytest.mark.weight(5)
@pytest.mark.number("2.6")
def test_algorithm_performance_discussion():
    """report.md: Performance Discussion check"""
    content = get_report_content()
    discussion_points = [
        "Which search algorithm is best for this route finding problem?",
        "Link the idea of search algorithm to today Generative AI."
    ]
    
    for idx, question in enumerate(discussion_points, 1):
        text = get_section_discussion_answer(question, content)
        assert text is not None, f"Discussion question {idx} ('{question}') is missing from report.md"
        text = text.strip()
        assert text != "", f"Discussion question {idx} ('{question}') has not been filled out (it is empty)"
        assert not (text.startswith("[") and text.endswith("]")), f"Discussion question {idx} ('{question}') cannot contain placeholder text"
