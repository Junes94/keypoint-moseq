import os
import uuid
import yaml
from bokeh.io import output_notebook, show
import ipywidgets as widgets
from IPython.display import display
from keypoint_moseq.widgets import GroupSettingWidgets, InteractiveVideoViewer, SyllableLabeler
from keypoint_moseq.io import load_results
output_notebook()

def interactive_group_setting(progress_paths):
    """start the interactive group setting widget

    Parameters
    ----------
    progress_paths : dict
        the dictionary containing the progress and the filepaths of the project

    Returns
    -------
    progress_paths : dict
        the dictionary containing the progress and the filepaths of the project with index path updated
    """

    index_filepath = os.path.join(progress_paths['base_dir'], 'index.yaml')

    if os.path.exists(index_filepath):
        with open(index_filepath, 'r') as f:
            index_data = yaml.safe_load(f)
    else:
        # generate a new index file
        results_dict = load_results(
            project_dir=progress_paths['base_dir'], name=progress_paths['model_name'])
        files = []
        for session in results_dict.keys():
            file_dict = {'filename': session, 'group': 'default',
                         'uuid': str(uuid.uuid4())}
            files.append(file_dict)

        index_data = {'files': files}
        # write to file and progress_paths
        with open(index_filepath, 'w') as f:
            yaml.safe_dump(index_data, f, default_flow_style=False)

    # update progress file to ensure index_file is in progress.yaml
    progress_paths['index_file'] = index_filepath
    with open(progress_paths['progress_filepath'], 'w') as f:
        yaml.safe_dump(progress_paths, f, default_flow_style=False)

    # display the widget
    index_grid = GroupSettingWidgets(index_filepath)
    display(index_grid.clear_button, index_grid.group_set)
    display(index_grid.qgrid_widget)

    return progress_paths


def view_syllable_movies(progress_paths, movie_type='grid'):
    """view the syllable grid movie or crowd movie

    Parameters
    ----------
    progress_paths : dict
        the dictionary containing path names in the analysis process
    type : str, optional
        the type of movie to view, by default 'grid'
    """

    output_notebook()
    if movie_type == 'grid':
        # show grid movies
        video_dir = os.path.join(progress_paths['model_dir'], 'grid_movies')
        viewer = InteractiveVideoViewer(syll_vid_dir=video_dir)
    else:
        # show crowd movies
        video_dir = os.path.join(progress_paths['model_dir'], 'crowd_movies')
        viewer = InteractiveVideoViewer(syll_vid_dir=video_dir)

    # Run interactive application
    selout = widgets.interactive_output(viewer.get_video,
                                        {'input_file': viewer.sess_select})
    display(viewer.clear_button, viewer.sess_select, selout)


def label_syllables(progress_paths, movie_type='grid'):
    """label syllables in the syllable grid movie

    Parameters
    ----------
    progress_paths : dict
        the dictionary containing path names in the analysis process
    """

    output_notebook()

    # check if syll_info.yaml exists
    syll_info_path = progress_paths.get('syll_info_path', None)
    if syll_info_path is None:
        syll_info_path = os.path.join(
            progress_paths['base_dir'], 'syll_info.yaml')
        progress_paths['syll_info_path'] = syll_info_path
        with open(progress_paths['progress_filepath'], 'w') as f:
            yaml.safe_dump(progress_paths, f, default_flow_style=False)


    labeler = SyllableLabeler(progress_paths['base_dir'], progress_paths['model_name'],
                              progress_paths['index_file'], movie_type, progress_paths['syll_info_path'])
    output = widgets.interactive_output(labeler.interactive_syllable_labeler, {'syllables': labeler.syll_select})
    display(labeler.clear_button, labeler.syll_select, output)

    return progress_paths