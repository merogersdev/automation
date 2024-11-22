from re import sub, split, search
from os import scandir


def rename_video(file, encoder_info):
    # Renames video based on type of file - eg. tv episode or video
    episode_regex = r"\w{1}\d{1,2}\w{1}\d{2}"
    episode = search(episode_regex, file)
    year_regex = r"\d{4}"
    year = search(year_regex, file)
    special_regex = r"[^\w\d\.]*"

    replacements = [
        (" ", "."),
        (special_regex, ""),
        (r"[\.]{2,}", ".")
    ]

    # If no year present in filename, just omit
    if year == None:
        year_made = ""
    else:
        year_made = year.group()

    if episode:
        file_segments = split(episode_regex, file)
        new_title = file_segments[0]
        for old, new in replacements:
            new_title = sub(old, new, new_title)

        return f"{new_title}{episode.group()}{encoder_info}"
    file_segments = split(year_regex, file)
    new_title = file_segments[0]
    for old, new in replacements:
        new_title = sub(old, new, new_title)
    return f"{new_title}{year_made}{encoder_info}"


def get_resolution(filename):
    # Looks for HD formats in file or returns a . for standard/unknown definition so filename can be structured correctly
    hd_regex = r"\.?(1080p|720p|2160p|4[kK])\.?"
    has_resolution = search(hd_regex, filename)

    if has_resolution != None:
        resolution = has_resolution.group()
        resolution = sub(r"\.", "", resolution)
        return f".{resolution}."
    return "."


def sort_files(directory):
    # Sorts files alphabetically
    with scandir(directory) as entries:
        sorted_entries = sorted(entries, key=lambda entry: entry.name)
        sorted_items = [entry.name for entry in sorted_entries]
    return sorted_items
