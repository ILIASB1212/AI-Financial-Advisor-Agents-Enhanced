from agents import function_tool

@function_tool
def markdown_generator_tool(report_content: str, file_name: str) -> str:
    """
    Formats raw text content into professional Markdown and returns it directly for UI display.
    The file_name parameter is accepted but can be used for context (not for saving files).
    
    Args:
        report_content: The full text content of the final report, ready for formatting.
        file_name: The desired output file name (used for context only, not saved).
    
    Returns:
        The formatted markdown content as a string ready for UI display.
    """
    formatted_content = report_content
    

    if formatted_content and not formatted_content.startswith('#'):
        formatted_content = f"# {file_name}\n\n{formatted_content}"
    
    return formatted_content