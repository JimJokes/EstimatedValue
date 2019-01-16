import Tkinter as tk
from ScrolledText import ScrolledText
import sys
import math

import requests
import threading
import urllib2

import myNotebook as nb
from config import config

if __debug__:
    from traceback import print_exc

VERSION = '0.01'

EDSM_API = 'https://www.edsm.net/api-system-v1/bodies?systemName=%s&systemId64=%s'

this = sys.modules[__name__]  # For holding module globals
this.frame = None
this.body_lists = []
this.edsm_session = None
this.edsm_data = None
this.enable = config.getint('enable_est')

Terraformed = 'Terraformed'
Candidate = 'Candidate for terraforming'


class EDStarType:
    UNKNOWN = None

    O = 'O'
    OStar = 'O (Blue-White) Star'
    B = 'B'
    BStar = 'B (Blue-White) Star'
    A = 'A'
    AStar = 'A (Blue-White) Star'
    F = 'F'
    FStar = 'F (White) Star'
    G = 'G'
    GStar = 'G (White-Yellow) Star'
    K = 'K'
    KStar = 'K (Yellow-Orange) Star'
    M = 'M'
    MStar = 'M (Red dwarf) Star'

    # Dwarf
    L = 'L'
    LStar = 'L (Brown dwarf) Star'
    T = 'T'
    TStar = 'T (Brown dwarf) Star'
    Y = 'Y'
    YStar = 'Y (Brown dwarf) Star'

    # proto stars
    AeBe = 'AeBe'
    AeBeStar = 'Herbig Ae/Be Star'
    TTS = 'TTS'
    TTSStar = 'T Tauri Star'

    # wolf rayet
    W = 'W'
    WStar = 'Wolf-Rayet Star'
    WN = 'WN'
    WNStar = 'Wolf-Rayet N Star'
    WNC = 'WNC'
    WNCStar = 'Wolf-Rayet NC Star'
    WC = 'WC'
    WCStar = 'Wolf-Rayet C Star'
    WO = 'WO'
    WOStar = 'Wolf-Rayet O Star'

    # Carbon
    CS = 'CS'
    C = 'C'
    CStar = 'C Star'
    CN = 'CN'
    CNStar = 'CN Star'
    CJ = 'CJ'
    CJStar = 'CJ Star'
    CHd = 'CHd'

    MS = 'MS'
    MSStar = 'MS-type Star'
    S = 'S'
    SStar = 'S-type Star'

    # white dwarf
    D = 'D'
    DStar = 'White Dwarf (D) Star'
    DA = 'DA'
    DAStar = 'White Dwarf (DA) Star'
    DAB = 'DAB'
    DABStar = 'White Dwarf (DAB) Star'
    DAO = 'DAO'
    DAZ = 'DAZ'
    DAZStar = 'White Dwarf (DAZ) Star'
    DAV = 'DAV'
    DAVStar = 'White Dwarf (DAV) Star'
    DB = 'DB'
    DBStar = 'White Dwarf (DB) Star'
    DBZ = 'DBZ'
    DBZStar = 'White Dwarf (DBZ) Star'
    DBV = 'DBV'
    DBVStar = 'White Dwarf (DBV) Star'
    DO = 'DO'
    DOV = 'DOV'
    DQ = 'DQ'
    DQStar = 'White Dwarf (DQ) Star'
    DC = 'DC'
    DCStar = 'White Dwarf (DC) Star'
    DCV = 'DCV'
    DCVStar = 'White Dwarf (DCV) Star'
    DX = 'DX'

    N = 'N'  # Neutron
    NStar = 'Neutron Star'

    H = 'H'  # Black Hole
    HStar = 'Black Hole'

    X = 'X'  # currently speculative, not confirmed with actual data... in journal

    A_BlueWhiteSuperGiant = 'ABlueWhiteSuperGiant'
    AStar_BlueWhiteSuperGiant = 'A (Blue-White super giant) Star'
    F_WhiteSuperGiant = 'FWhiteSuperGiant'
    FStar_WhiteSuperGiant = 'F (White super giant) Star'
    M_RedSuperGiant = 'MRedSuperGiant'
    MStar_RedSuperGiant = 'M (Red super giant) Star'
    M_RedGiant = 'MRedGiant'
    MStar_RedGiant = 'M (Red giant) Star'
    K_OrangeGiant = 'KOrangeGiant'
    KStar_OrangeGiant = 'K (Yellow-Orange giant) Star'
    RoguePlanet = 'RoguePlanet'
    Nebula = 'Nebula'
    StellarRemnantNebula = 'StellarRemnantNebula'
    SuperMassiveBlackHole = 'SuperMassiveBlackHole'
    SuperMassiveBlackHoleStar = 'Supermassive Black Hole'

    def __init__(self):
        pass


class EDPlanetType:
    UNKNOWN = None

    Metal_rich_body = 'Metalrichbody'
    High_metal_content_body = 'Highmetalcontentbody'
    High_metal_content_world = 'Highmetalcontentworld'
    Rocky_body = 'Rockybody'
    Icy_body = 'Icybody'
    Rocky_ice_body = 'Rockyicebody'
    Rocky_ice_world = 'Rockyiceworld'
    Earthlike_body = 'Earthlikebody'
    Earthlike_world = 'Earthlikeworld'
    Water_world = 'Waterworld'
    Ammonia_world = 'Ammoniaworld'
    Water_giant = 'Watergiant'
    Water_giant_with_life = 'Watergiantwithlife'
    Gas_giant_with_water_based_life = 'Gasgiantwithwaterbasedlife'
    Gas_giant_with_ammonia_based_life = 'Gasgiantwithammoniabasedlife'
    Sudarsky_class_I_gas_giant = 'SudarskyclassIgasgiant'
    Class_I_gas_giant = 'ClassIgasgiant'
    Sudarsky_class_II_gas_giant = 'SudarskyclassIIgasgiant'
    Class_II_gas_giant = 'ClassIIgasgiant'
    Sudarsky_class_III_gas_giant = 'SudarskyclassIIIgas giant'
    Class_III_gas_giant = 'ClassIIIgas giant'
    Sudarsky_class_IV_gas_giant = 'SudarskyclassIVgasgiant'
    Class_IV_gas_giant = 'ClassIVgasgiant'
    Sudarsky_class_V_gas_giant = 'SudarskyclassVgasgiant'
    Class_V_gas_giant = 'ClassVgasgiant'
    Helium_rich_gas_giant = 'Heliumrichgasgiant'
    Helium_gas_giant = 'Heliumgasgiant'

    # Custom types
    High_metal_content_body_700 = 'Highmetalcontentbody700'
    High_metal_content_body_250 = 'Highmetalcontentbody250'
    High_metal_content_body_hot_thick = 'Highmetalcontentbodyhotthick'

    def __init__(self):
        pass


class Body:
    value = None
    bonus = 0

    def __init__(self, entry, edsm=False):
        self.name = entry.get('BodyName') if not edsm else entry.get('name')
        self.isStar = True if (not edsm and entry.get('StarType')) or (edsm and entry.get('type') == 'Star') else False
        self.isPlanet = True if (not edsm and entry.get('PlanetClass')) or (edsm and entry.get('type') == 'Planet') \
            else False

        if self.isStar:
            self.starType = entry.get('StarType').replace('-', '').replace(' ', '').replace('_', '') if not edsm else \
                entry.get('subType')
            self.stellarMass = entry.get('StellarMass') or 1.0 if not edsm else entry.get('solarMasses') or 1.0

        elif self.isPlanet:
            self.planetType = entry.get('PlanetClass').replace('-', '').replace(' ', '').replace('_', '') if not edsm \
                else entry.get('subType').replace('-', '').replace(' ', '').replace('_', '')
            self.terraformable = True if (not edsm and entry.get('TerraformState')) or (
                    edsm and entry.get('terraformingState') in [Terraformed, Candidate]) else False
            self.massEM = entry.get('MassEM') or 1.0 if not edsm else entry.get('earthMasses') or 1.0

    def is_star_or_planet(self):
        return self.isStar or self.isPlanet

    def calculate_value(self):
        if self.isStar:

            if self.starType in [EDStarType.D, EDStarType.DA, EDStarType.DAB, EDStarType.DAO, EDStarType.DAZ,
                                 EDStarType.DAV, EDStarType.DB, EDStarType.DBZ, EDStarType.DBV, EDStarType.DO,
                                 EDStarType.DOV, EDStarType.DQ, EDStarType.DC, EDStarType.DCV, EDStarType.DX] \
                    or self.starType in [EDStarType.DStar, EDStarType.DAStar, EDStarType.DABStar, EDStarType.DAZStar,
                                         EDStarType.DAVStar, EDStarType.DBStar, EDStarType.DBZStar, EDStarType.DBVStar,
                                         EDStarType.DQStar, EDStarType.DCStar, EDStarType.DCVStar]:
                self.value = 33737

            elif self.starType in [EDStarType.N, EDStarType.NStar, EDStarType.H, EDStarType.HStar]:
                self.value = 54309

            elif self.starType in [EDStarType.SuperMassiveBlackHole, EDStarType.SuperMassiveBlackHoleStar]:
                self.value = 80.5654

            else:
                self.value = 2880

            return str(int(round(star_value(self.value, self.stellarMass))))

        elif self.isPlanet:

            if self.planetType in [EDPlanetType.Metal_rich_body]:
                self.value = 52292

            elif self.planetType in [EDPlanetType.High_metal_content_body, EDPlanetType.High_metal_content_world,
                                     EDPlanetType.Sudarsky_class_II_gas_giant, EDPlanetType.Class_II_gas_giant]:
                self.value = 23168
                if self.terraformable:
                    self.bonus = 241607

            elif self.planetType in [EDPlanetType.Earthlike_body, EDPlanetType.Earthlike_world]:
                self.value = 155581
                self.bonus = 279088

            elif self.planetType in [EDPlanetType.Water_world]:
                self.value = 155581
                if self.terraformable:
                    self.bonus = 279088

            elif self.planetType in [EDPlanetType.Ammonia_world]:
                self.value = 232619

            elif self.planetType in [EDPlanetType.Sudarsky_class_I_gas_giant, EDPlanetType.Class_I_gas_giant]:
                self.value = 3974

            else:
                self.value = 720
                if self.terraformable:
                    self.bonus = 223971

            value = planet_value(self.value, self.massEM)
            if self.terraformable or self.planetType in [EDPlanetType.Earthlike_body, EDPlanetType.Earthlike_world]:
                value += planet_value(self.bonus, self.massEM)

            return str(int(round(value)))

        else:
            return '0'


def star_value(k, m):
    return k + (m * k / 66.25)


def planet_value(k, m):
    return k + (3 * k * math.pow(m, 0.199977) / 5.3)


def plugin_start():
    return 'EstimatedValue'


def plugin_app(parent):
    # Create and display widgets
    this.frame = ScrolledText(parent, height=10, state=tk.DISABLED, borderwidth=0, width=50, cursor='')
    this.frame.bind('<<EstimatedValue>>', parse_edsm_data)  # callback when EDSM data received
    this.frame.bind('<Configure>', reset_tabstop)  # reset tab stop
    return this.frame


def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    # nb.Label(frame, text='Enable plugin?').grid(row=0, padx=10, pady=(10, 0), sticky=tk.W)
    # this.config_enable = tk.IntVar(value=this.enable)
    # nb.Checkbutton(frame, text='Enable EstimatedValue', variable=this.config_enable).grid(row=1, padx=10, pady=2,
    #                                                                                       sticky=tk.W)
    nb.Label(frame, text='Version %s' % VERSION).grid(padx=10, pady=10, sticky=tk.W)
    return frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    # print '\033[1;33m' + entry['event'] + '\033[0m'
    if entry['event'] == 'Scan':
        body = Body(entry)
        need_update = update_body_list(body)
        if need_update:
            update_frame()
        return
    elif entry['event'] in ['FSDJump', 'Location', 'StartUp']:
        thread = threading.Thread(target=edsm_worker, name='EDSM lookup',
                                  args=(entry.get('StarSystem', system), entry.get('SystemAddress', '')))
        thread.daemon = True
        thread.start()


# EDSM lookup
def edsm_worker(system_name, system_id):
    if not this.edsm_session:
        this.edsm_session = requests.Session()

    try:
        r = this.edsm_session.get(EDSM_API % (urllib2.quote(system_name), system_id), timeout=10)
        r.raise_for_status()
        this.edsm_data = r.json() or {}  # Unknown system represented as empty list
    except:
        this.edsm_data = None

    # Tk is not thread-safe, so can't access widgets in this thread.
    # event_generate() is the only safe way to poke the main thread from this thread.
    this.frame.event_generate('<<EstimatedValue>>', when='tail')


# EDSM data parse
def parse_edsm_data(event):
    this.body_lists = []
    if this.edsm_data:
        for b in this.edsm_data.get('bodies', []):
            body = Body(b, edsm=True)
            update_body_list(body)

    update_frame()


def update_frame():
    this.frame['state'] = tk.NORMAL
    this.frame.delete('1.0', tk.END)
    this.body_lists.sort(key=lambda b: int(b[1]), reverse=True)

    for (name, value) in this.body_lists:
        this.frame.insert(tk.END, name + '\t' + value + ' Cr\n')
    this.frame['state'] = tk.DISABLED


def update_body_list(body):
    if body is None or body.name is None or not body.is_star_or_planet():
        return False
    for index, (name, value) in enumerate(this.body_lists):
        if body.name == name:
            this.body_lists[index] = (body.name, body.calculate_value())
            return True

    this.body_lists.append((body.name, body.calculate_value()))
    return True


def reset_tabstop(event):
    event.widget.configure(tabs=(event.width - 8, "right"))  # right-justified tab stop


def test():
    thread = threading.Thread(target=edsm_worker, name='EDSM lookup', args=('Blu Thua EW-O b34-1',))
    thread.daemon = True
    thread.start()
