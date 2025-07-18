from pathlib import Path
from typing import Union

ERROR_NOT_FIND_DESKTOP = 10
ERROR_NOT_FIND_MAIN_FILE = 11
ERROR_NOT_FIND_SCAN_FILE = 12
ERROR_NOT_FIND_MENU_DIR = 13
CATEGORIES_OFFICE = 'Office;Viewer;Scanning;'


# Main Categories:
# Audio;Video;Development;Education;
# Game;Graphics;Network;Office;Settings;Utility;

# Additional categories:
# Building;Debugger;IDE;GUIDesigner;Profiling;RevisionControl;Translation;Calendar;
# ContactManagement;Database;Dictionary;Chart;Email;Finance;FlowChart;PDA;ProjectManagement;
# Presentation;Spreadsheet;WordProcessor;2DGraphics;VectorGraphics;RasterGraphics;3DGraphics;
# Scanning;OCR;Photography;Publishing;Viewer;TextTools;DesktopSettings;HardwareSettings;
# Printing;PackageManager;Dialup;InstantMessaging;Chat;IRCClient;FileTransfer;HamRadio;
# News;P2P;RemoteAccess;Telephony;TelephonyTools;VideoConference;WebBrowser;WebDevelopment;
# Midi;Mixer;Sequencer;Tuner;TV;AudioVideoEditing;Player;Recorder;DiscBurning;ActionGame;
# AdventureGame;ArcadeGame;BoardGame;BlocksGame;CardGame;KidsGame;LogicGame;RolePlaying;
# Simulation;SportsGame;StrategyGame;Art;Construction;Music;Languages;Science;
# ArtificialIntelligence;Astronomy;Biology;Chemistry;ComputerScience;DataVisualization;
# Economy;Electricity;Geography;Geology;Geoscience;History;ImageProcessing;Literature;
# Math;NumericalAnalysis;MedicalSoftware;Physics;Robotics;Sports;ParallelComputing;
# Amusement;Archiving;Compression;Electronics;Emulator;Engineering;FileTools;FileManager;
# TerminalEmulator;Filesystem;Monitor;Security;Accessibility;Calculator;Clock;TextEditor;
# Documentation;Core;KDE;GNOME;GTK;Qt;Motif;Java;ConsoleOnly;

def create_desktop_entry(name: str, file_name: Union[Path, str], icon: Union[Path, str] = None, comment: str = None,
                         desktop=True, menu=False, categories=None):
    """Создает ярлыки для основной программы и сканера.
    :param name: Названия ярлыка;
    :param file_name: Имя исполняемого файла в рабочей директории;
    :param icon: Имя файла изображения в рабочей директории;
    :param comment: Комментарий;
    :param desktop: Создать ярлык на рабочем столе;
    :param menu: Создать ярлык в меню системы;
    :param categories: Указать в какой категории размещать ярлык.
    :return: Возвращает номер ошибки или None.
    """
    if isinstance(file_name, str):
        file_name = Path(file_name)
    if icon is not None and isinstance(icon, str):
        icon = Path(icon)
    current_dir = Path.cwd()
    exec_file = current_dir / file_name

    content_label = ['[Desktop Entry]',
                     'Type=Application',
                     'Terminal=false',
                     f'Name={name}',
                     f'Exec={exec_file}',
                     f'Path={current_dir}',
                     ]
    if icon is not None:
        content_label.append(f'Icon={current_dir / icon}')
    if comment is not None:
        content_label.append(f'Comment={comment}')

    if exec_file.exists():
        if desktop:
            # Путь к директории рабочего стола текущего пользователя
            desktop_dir = Path.home() / 'Desktop'
            if not desktop_dir.is_dir():
                desktop_dir = Path.home() / 'Рабочий стол'
                if not desktop_dir.is_dir():
                    return ERROR_NOT_FIND_DESKTOP

            file_path = desktop_dir / f'{name}.desktop'
            with file_path.open('w') as fp:
                for s in content_label:
                    fp.write(s)
                    fp.write('\n')
            file_path.chmod(0o755)
        if menu:
            menu_dir = Path('/usr/share/applications')
            if not menu_dir.is_dir():
                return ERROR_NOT_FIND_MENU_DIR
            if categories is not None:
                content_label.append(f'Categories={categories}')
            file_path = menu_dir / f'{name}.desktop'
            with file_path.open('w') as fp:
                for s in content_label:
                    fp.write(s)
                    fp.write('\n')
            file_path.chmod(0o755)
        return None

    else:
        return ERROR_NOT_FIND_MAIN_FILE
