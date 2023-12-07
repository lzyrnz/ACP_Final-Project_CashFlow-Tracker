def update_theme():
    theme_color = "#2A8C55" if not dark_mode_enabled else "#333333"  # Adjust color based on dark mode
    bg_color = "#B2C8BA" if not dark_mode_enabled else "#1a1a1a"  # Adjust background color based on dark mode

    # Update sidebar frame
    sidebar_frame.configure(fg_color=theme_color)

    # Update mainframe
    mainframe.configure(fg_color=bg_color)

    # Update summary frame
    summary_frame.configure(fg_color=theme_color)

    # Update bottom frame
    bottomframe.configure(fg_color=theme_color)

    # Update labels
    account_name_label.configure(text_color="white")

    # Update buttons
    dark_mode_button.configure(fg_color="#2A8C55", hover_color="#2A8C55")
    sort_button.configure(fg_color="#33b249", hover_color="#B2C8BA")
    sort2_button.configure(fg_color="#33b249", hover_color="#B2C8BA")
    show_graph_button.configure(fg_color="#33b249", hover_color="#B2C8BA")