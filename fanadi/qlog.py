import ctypes
import array

from fanadi.data_types import *
from fanadi.util import *

class c_xyz(ctypes.BigEndianStructure): # Size: 0xC
    _pack_ = 1
    _fields_ = [
        ("x", ctypes.c_float),                      # 0x00
        ("y", ctypes.c_float),                      # 0x04
        ("z", ctypes.c_float),                      # 0x08
    ]
assert(ctypes.sizeof(c_xyz) == 0xC)

class c_player_status_a(ctypes.BigEndianStructure): # Size: 0x28
    class c_select_equip(ctypes.BigEndianStructure): # Size: 0x06
        _pack_ = 1
        _fields_ = [
            ("Clothing", ctypes.c_uint8),           # 0x00
            ("Sword", ctypes.c_uint8),              # 0x01
            ("Shield", ctypes.c_uint8),             # 0x02
            ("Smell", ctypes.c_uint8),              # 0x03
            ("BButton", ctypes.c_uint8),            # 0x04
            ("_padding", ctypes.c_uint8)            # 0x05
        ]

        _field_ui_types_ = {
            "Clothing": e_item_clothing,
            "Sword": e_item_sword,
            "Shield": e_item_shield,
            "Smell": e_item_smell,
            "BButton": e_item
        }

    class c_select_item(ctypes.BigEndianStructure): # Size: 0x04
        _pack_ = 1
        _fields_ = [
            ("XLeft", ctypes.c_uint8),              # 0x00
            ("YRight", ctypes.c_uint8),             # 0x01
            ("Down", ctypes.c_uint8),               # 0x02
            ("B", ctypes.c_uint8),                  # 0x03
        ]

        _field_ui_types_ = {
            "XLeft": e_item_slot,
            "YRight": e_item_slot,
            "Down": e_item_slot,
            "B": e_item_slot
        }

    class c_mix_item(ctypes.BigEndianStructure): # Size: 0x04
        _pack_ = 1
        _fields_ = [
            ("XLeft", ctypes.c_uint8),              # 0x00
            ("YRight", ctypes.c_uint8),             # 0x01
            ("Down", ctypes.c_uint8),               # 0x02
            ("B", ctypes.c_uint8),                  # 0x03
        ]

        _field_ui_types_ = {
            "XLeft": e_item_slot,
            "YRight": e_item_slot,
            "Down": e_item_slot,
            "B": e_item_slot
        }

    _pack_ = 1
    _fields_ = [
        ("MaxLife", ctypes.c_uint16),               # 0x00
        ("Life", ctypes.c_uint16),                  # 0x02
        ("Rupee", ctypes.c_uint16),                 # 0x04
        ("MaxOil", ctypes.c_uint16),                # 0x06
        ("Oil", ctypes.c_uint16),                   # 0x08
        ("unk10", ctypes.c_uint8),                  # 0x0A
        ("SelectItem", c_select_item),              # 0x0B
        ("MixItem", c_mix_item),                    # 0x0F
        ("SelectEquip", c_select_equip),            # 0x13
        ("WalletSize", ctypes.c_uint8),             # 0x19
        ("MaxMagic", ctypes.c_uint8),               # 0x1A
        ("Magic", ctypes.c_uint8),                  # 0x1B
        ("MagicFlag", ctypes.c_uint8),              # 0x1C
        ("unk29", ctypes.c_uint8),                  # 0x1D
        ("TransformStatus", ctypes.c_uint8),        # 0x1E
        ("unk31", ctypes.c_uint8 * 3),              # 0x1F
        ("_padding", ctypes.c_uint8 * 6),           # 0x22
    ]

    _field_ui_types_ = {
        "WalletSize": e_wallets,
        "TransformStatus": e_transform_status
    }

assert(ctypes.sizeof(c_player_status_a) == 0x28)


class c_player_status_b(ctypes.BigEndianStructure): # Size: 0x18
    _pack_ = 1
    _fields_ = [
        ("DateIpl", ctypes.c_int64),                # 0x00
        ("TransformLevelFlag", ctypes.c_uint8),     # 0x08
        ("DarkClearLevelFlag", ctypes.c_uint8),     # 0x09
        ("unk10", ctypes.c_uint8),                  # 0x0A
        ("unk11", ctypes.c_uint8),                  # 0x0B
        ("Time", ctypes.c_float),                   # 0x0C
        ("Date", ctypes.c_uint16),                  # 0x10
        ("unk18", ctypes.c_uint8 * 3),              # 0x12
        ("_padding", ctypes.c_uint8 * 3),           # 0x15
    ]
assert(ctypes.sizeof(c_player_status_b) == 0x18)


class c_horse_place(ctypes.BigEndianStructure): # Size: 0x18
    _pack_ = 1
    _fields_ = [
        ("Pos", c_xyz),                             # 0x00
        ("AngleY", ctypes.c_int16),                 # 0x0C
        ("Name", ctypes.c_char * 8),                # 0x0E
        ("SpawnId", ctypes.c_uint8),                # 0x16
        ("RoomNo", ctypes.c_int8),                  # 0x17
    ]
assert(ctypes.sizeof(c_horse_place) == 0x18)


class c_player_return_place(ctypes.BigEndianStructure): # Size: 0xC
    _pack_ = 1
    _fields_ = [
        ("Name", ctypes.c_char * 8),                # 0x00
        ("PlayerStatus", ctypes.c_uint8),           # 0x08
        ("RoomNo", ctypes.c_int8),                  # 0x09
        ("unk10", ctypes.c_uint8),                  # 0x0A
        ("unk11", ctypes.c_uint8),                  # 0x0B
    ]
assert(ctypes.sizeof(c_player_return_place) == 0xC)


class c_player_field_last_stay_info(ctypes.BigEndianStructure): # Size: 0x1C
    _pack_ = 1
    _fields_ = [
        ("Pos", c_xyz),                             # 0x00
        ("AngleY", ctypes.c_int16),                 # 0x0C
        ("Name", ctypes.c_char * 8),                # 0x0E
        ("LastSpawnId", ctypes.c_int8),             # 0x16
        ("RegionNo", ctypes.c_uint8),               # 0x17
        ("FieldDataExistFlag", ctypes.c_uint8),     # 0x18
        ("Region", ctypes.c_uint8),                 # 0x19
        ("unk26", ctypes.c_uint8 * 2),              # 0x1A
    ]
assert(ctypes.sizeof(c_player_field_last_stay_info) == 0x1C)


class c_player_last_mark_info(ctypes.BigEndianStructure): # Size: 0x1C
    _pack_ = 1
    _fields_ = [
        ("Pos", c_xyz),                             # 0x00
        ("AngleY", ctypes.c_int16),                 # 0x0C
        ("Name", ctypes.c_char * 8),                # 0x0E
        ("LastSpawnId", ctypes.c_int8),             # 0x16 
        ("RegionNo", ctypes.c_uint8),               # 0x17
        ("FieldDataExistFlag", ctypes.c_uint8),     # 0x18
        ("Region", ctypes.c_uint8),                 # 0x19
        ("unk26", ctypes.c_uint8 * 2),              # 0x1A
    ]
assert(ctypes.sizeof(c_player_last_mark_info) == 0x1C)


class c_player_item(ctypes.BigEndianStructure): # Size: 0x30
    _pack_ = 1
    _fields_ = [
        ("Items", ctypes.c_uint8 * 24),             # 0x00
        ("ItemSlots", ctypes.c_uint8 * 24),         # 0x18
    ]

    _field_ui_types_ = {
        "Items": e_item,
        "ItemSlots": e_item_slot
    }
assert(ctypes.sizeof(c_player_item) == 0x30)


class c_player_get_item(ctypes.BigEndianStructure): # Size: 0x20
    _pack_ = 1
    _fields_ = [
        ("ItemFlags", ctypes.c_uint32 * 8),         # 0x00
    ]
assert(ctypes.sizeof(c_player_get_item) == 0x20)


class c_player_item_record(ctypes.BigEndianStructure): # Size: 0xC
    _pack_ = 1
    _fields_ = [
        ("ArrowNum", ctypes.c_uint8),               # 0x00
        ("BombNum", ctypes.c_uint8 * 3),            # 0x01
        ("BottleNum", ctypes.c_uint8 * 4),          # 0x04
        ("PachinkoNum", ctypes.c_uint8),            # 0x08
        ("unk5", ctypes.c_uint8 * 3),               # 0x09
    ]
assert(ctypes.sizeof(c_player_item_record) == 0xC)


class c_player_item_max(ctypes.BigEndianStructure): # Size: 0x8
    _pack_ = 1
    _fields_ = [
        ("ItemMax", ctypes.c_uint8 * 8),           # 0x00
    ]
assert(ctypes.sizeof(c_player_item_max) == 0x8)


class c_player_collect(ctypes.BigEndianStructure): # Size: 0x10
    _pack_ = 1
    _fields_ = [
        ("Item", ctypes.c_uint8 * 8),               # 0x00
        ("unk8", ctypes.c_uint8),                   # 0x08
        ("Crystal", ctypes.c_uint8),                # 0x09
        ("Mirror", ctypes.c_uint8),                 # 0x0A
        ("unk11", ctypes.c_uint8),                  # 0x0B
        ("PohNum", ctypes.c_uint8),                 # 0x0C
        ("padding", ctypes.c_uint8 * 3),            # 0x0D
    ]
assert(ctypes.sizeof(c_player_collect) == 0x10)


class c_player_wolf(ctypes.BigEndianStructure): # Size: 0x4
    _pack_ = 1
    _fields_ = [
        ("unk0", ctypes.c_uint8 * 3),               # 0x00
        ("unk3", ctypes.c_uint8),                   # 0x03
    ]
assert(ctypes.sizeof(c_player_wolf) == 0x4)


class c_light_drop(ctypes.BigEndianStructure): # Size: 0x8
    _pack_ = 1
    _fields_ = [
        ("LightDropNum", ctypes.c_uint8 * 4),       # 0x00
        ("LightDropGetFlag", ctypes.c_uint8),       # 0x04
        ("unk5", ctypes.c_uint8 * 3),               # 0x05
    ]
assert(ctypes.sizeof(c_light_drop) == 0x8)


class c_letter_info(ctypes.BigEndianStructure): # Size: 0x50
    _pack_ = 1
    _fields_ = [
        ("LetterGetFlags", ctypes.c_uint32 * 2),    # 0x00
        ("LetterReadFlags", ctypes.c_uint32 * 2),   # 0x08
        ("GetNumber", ctypes.c_uint8 * 64),         # 0x10
    ]
assert(ctypes.sizeof(c_letter_info) == 0x50)


class c_fishing_info(ctypes.BigEndianStructure): # Size: 0x34
    _pack_ = 1
    _fields_ = [
        ("FishCount", ctypes.c_uint16 * 16),        # 0x00
        ("MaxSize", ctypes.c_uint8 * 16),           # 0x20
        ("_padding", ctypes.c_uint8 * 4),           # 0x30
    ]
assert(ctypes.sizeof(c_fishing_info) == 0x34)


class c_player_info(ctypes.BigEndianStructure): # Size: 0x40
    _pack_ = 1
    _fields_ = [
        ("unk0", ctypes.c_uint64),                  # 0x00
        ("TotalTime", ctypes.c_int64),              # 0x08
        ("unk16", ctypes.c_uint16),                 # 0x10
        ("DeathCount", ctypes.c_uint16),            # 0x12
        ("PlayerName", ctypes.c_char * 16),         # 0x14
        ("unk36", ctypes.c_uint8),                  # 0x24
        ("HorseName", ctypes.c_char * 16),          # 0x25
        ("unk53", ctypes.c_uint8),                  # 0x35
        ("ClearCount", ctypes.c_uint8),             # 0x36
        ("unk55", ctypes.c_uint8 * 5),              # 0x37
        ("_padding", ctypes.c_uint8 * 4),           # 0x3C
    ]
assert(ctypes.sizeof(c_player_info) == 0x40)


class c_player_config(ctypes.BigEndianStructure): # Size: 0xC
    _pack_ = 1
    _fields_ = [
        ("FuriganaOff", ctypes.c_uint8),            # 0x00
        ("SoundMode", ctypes.c_uint8),              # 0x01
        ("AttentionType", ctypes.c_uint8),          # 0x02
        ("Vibration", ctypes.c_uint8),              # 0x03
        ("Language", ctypes.c_uint8),               # 0x04
        ("unk5", ctypes.c_uint8),                   # 0x05
        ("CalibrateDist", ctypes.c_uint16),         # 0x06
        ("CalValue", ctypes.c_uint8),               # 0x08
        ("ShortCut", ctypes.c_uint8),               # 0x09
        ("CameraControl", ctypes.c_uint8),          # 0x0A
        ("Pointer", ctypes.c_uint8),                # 0x0B
    ]

    _field_ui_types_ = {
        "FuriganaOff": e_boolean,
        "SoundMode": e_sound_mode,
        "AttentionType": e_attention_type,
        "Vibration": e_boolean,
        "Language": e_language,
        "ShortCut": e_boolean,
        "CameraControl": e_camera_control,
        "Pointer": e_boolean
    }
assert(ctypes.sizeof(c_player_config) == 0xC)


class c_player(ctypes.BigEndianStructure): # Size: 0x1EC
    _pack_ = 1
    _fields_ = [
        ("PlayerStatusA", c_player_status_a),                           # 0x000
        ("PlayerStatusB", c_player_status_b),                           # 0x028
        ("HorsePlace", c_horse_place),                                  # 0x040
        ("PlayerReturnPlace", c_player_return_place),                   # 0x058
        ("PlayerFieldLastStayInfo", c_player_field_last_stay_info),     # 0x064
        ("PlayerLastMarkInfo", c_player_last_mark_info),                # 0x080
        ("Item", c_player_item),                                        # 0x09C
        ("GetItem", c_player_get_item),                                 # 0x0CC
        ("ItemRecord", c_player_item_record),                           # 0x0EC
        ("ItemMax", c_player_item_max),                                 # 0x0F8
        ("Collect", c_player_collect),                                  # 0x100
        ("Wolf", c_player_wolf),                                        # 0x110
        ("LightDrop", c_light_drop),                                    # 0x114
        ("LetterInfo", c_letter_info),                                  # 0x11C
        ("FishingInfo", c_fishing_info),                                # 0x16C
        ("PlayerInfo", c_player_info),                                  # 0x1A0
        ("Config", c_player_config),                                    # 0x1E0
    ]
assert(ctypes.sizeof(c_player) == 0x1EC)

class c_memory(ctypes.BigEndianStructure): # Size: 0x20
    _pack_ = 1
    _fields_ = [
        ("Tbox", ctypes.c_uint32 * 2),              # 0x00
        ("Switch", ctypes.c_uint32 * 4),            # 0x08
        ("Item", ctypes.c_uint32),                  # 0x18
        ("KeyNum", ctypes.c_uint8),                 # 0x1C
        ("DungeonItem", ctypes.c_uint8),            # 0x1D
        ("_padding", ctypes.c_uint8 * 2),           # 0x1E
    ]
assert(ctypes.sizeof(c_memory) == 0x20)


class c_event(ctypes.BigEndianStructure): # Size: 0x100
    _pack_ = 1
    _fields_ = [
        ("Event", ctypes.c_uint8 * 256),            # 0x00
    ]
assert(ctypes.sizeof(c_event) == 0x100)


class c_minigame(ctypes.BigEndianStructure): # Size: 0x18
    _pack_ = 1
    _fields_ = [
        ("unk0", ctypes.c_uint8 * 4),               # 0x00
        ("StarTime", ctypes.c_uint32),              # 0x04
        ("BalloonScore", ctypes.c_uint32),          # 0x08
        ("RaceGameTime", ctypes.c_uint32),          # 0x0C
        ("unk16", ctypes.c_uint32),                 # 0x10
        ("unk20", ctypes.c_uint32),                 # 0x14
    ]
assert(ctypes.sizeof(c_minigame) == 0x18)


class c_memory2(ctypes.BigEndianStructure): # Size: 0x8
    _pack_ = 1
    _fields_ = [
        ("VisitedRoom", ctypes.c_uint32 * 2),       # 0x00
    ]
assert(ctypes.sizeof(c_memory2) == 0x8)


class c_danbit(ctypes.BigEndianStructure): # Size: 0x3C
    _pack_ = 1
    _fields_ = [
        ("StageNo", ctypes.c_int8),                 # 0x00
        ("unk1", ctypes.c_uint8),                   # 0x01
        ("unk2", ctypes.c_uint8 * 2),               # 0x02
        ("Switch", ctypes.c_uint32 * 2),            # 0x04
        ("Item", ctypes.c_uint32 * 4),              # 0x0C
        ("unk28", ctypes.c_int16 * 16),             # 0x1C
    ]
assert(ctypes.sizeof(c_danbit) == 0x3C)


class c_zonebit(ctypes.BigEndianStructure): # Size: 0xE
    _pack_ = 1
    _fields_ = [
        ("Switch", ctypes.c_uint16 * 2),            # 0x00
        ("RoomSwitch", ctypes.c_uint16),            # 0x04
        ("Item", ctypes.c_uint16 * 2),              # 0x06
        ("RoomItem", ctypes.c_uint16),              # 0x0A
        ("unk12", ctypes.c_uint16),                 # 0x0C
    ]
assert(ctypes.sizeof(c_zonebit) == 0xE)


class c_zoneactor(ctypes.BigEndianStructure): # Size: 0x10
    _pack_ = 1
    _fields_ = [
        ("ActorFlags", ctypes.c_uint32 * 4),        # 0x00
    ]
assert(ctypes.sizeof(c_zoneactor) == 0x10)


class c_zone(ctypes.BigEndianStructure): # Size: 0x20
    _pack_ = 1
    _fields_ = [
        ("RoomNo", ctypes.c_int8),                  # 0x00
        ("unk1", ctypes.c_uint8),                   # 0x01
        ("Bit", c_zonebit),                         # 0x02
        ("Actor", c_zoneactor),                     # 0x10
    ]
assert(ctypes.sizeof(c_zone) == 0x20)


class c_restart(ctypes.BigEndianStructure): # Size: 0x24
    _pack_ = 1
    _fields_ = [
        ("RoomNo", ctypes.c_int8),                  # 0x00
        ("field_0x01", ctypes.c_uint8 * 3),         # 0x01
        ("StartPoint", ctypes.c_int16),             # 0x04
        ("RoomAngleY", ctypes.c_int16),             # 0x06
        ("RoomPos", c_xyz),                         # 0x08
        ("RoomParam", ctypes.c_uint32),             # 0x14
        ("LastSpeedF", ctypes.c_float),             # 0x18
        ("LastMode", ctypes.c_uint32),              # 0x1C
        ("LastAngleY", ctypes.c_int16),             # 0x20
        ("_padding", ctypes.c_int8 * 2),            # 0x22
    ]
assert(ctypes.sizeof(c_restart) == 0x24)


class c_turnrestart_camera(ctypes.BigEndianStructure): # Size: 0x24
    _pack_ = 1
    _fields_ = [
        ("CameraCtr", c_xyz),                       # 0x00
        ("CameraEye", c_xyz),                       # 0x0C
        ("CameraUp", c_xyz),                        # 0x18
    ]  
assert(ctypes.sizeof(c_turnrestart_camera) == 0x24)


class c_turnrestart(ctypes.BigEndianStructure): # Size: 0x3C
    _pack_ = 1
    _fields_ = [
        ("Position", c_xyz),                        # 0x00
        ("Param", ctypes.c_uint32),                 # 0x0C
        ("AngleY", ctypes.c_int16),                 # 0x10
        ("unk18", ctypes.c_int8),                   # 0x12
        ("_padding", ctypes.c_uint8 * 1),           # 0x13
        ("Camera", c_turnrestart_camera),           # 0x14
        ("CameraFvy", ctypes.c_float),              # 0x38
    ]
assert(ctypes.sizeof(c_turnrestart) == 0x3C)


class c_reserve(ctypes.BigEndianStructure): # Size: 0x50
    _pack_ = 1
    _fields_ = [
        ("unk", ctypes.c_uint8 * 80),
    ]
assert(ctypes.sizeof(c_reserve) == 0x50)


class c_save(ctypes.BigEndianStructure): # Size: 0x958
    _pack_ = 1
    _fields_ = [
        ("Player", c_player),                       # 0x000
        ("_padding", ctypes.c_uint8 * 4),           # 0x1EC
        ("Save", c_memory * 32),                    # 0x1F0
        ("Save2", c_memory2 * 64),                  # 0x5F0
        ("Event", c_event),                         # 0x7F0
        ("reserve", c_reserve),                     # 0x8F0
        ("MiniGame", c_minigame),                   # 0x940
    ]

    @classmethod
    def from_qlog_file(cls, filename: str):
        with open(filename, "rb") as f:
            ba = array.array("b")
            ba.fromfile(f, ctypes.sizeof(cls))
            return cls.from_buffer_copy(ba)

assert(ctypes.sizeof(c_save) == 0x958)

class c_qlog(ctypes.BigEndianStructure): # Size: 0xA94
    _pack_ = 1
    _fields_ = [
        ("Save", c_save),                           # 0x000
        ("unk0", ctypes.c_uint8 * 0x134),           # 0x95C
        ("Checksum", ctypes.c_uint64)               # 0xA8C
    ]

    def recalculate_checksum(self):
        self.Checksum = qlog_checksum(bytes(self)[:(ctypes.sizeof(c_qlog) - ctypes.sizeof(ctypes.c_uint64))])

    def to_bytes_without_checksum(self):
        return bytes(self)[:-ctypes.sizeof(ctypes.c_uint64)]

assert(ctypes.sizeof(c_qlog) == 0xA94)

class c_dat(ctypes.BigEndianStructure): # size: 0x2000
    _pack_ = 1
    _fields_ = [
        ("unk0", ctypes.c_uint32),                  # 0x0000
        ("DataVersion", ctypes.c_uint32),           # 0x0004
        ("Log1", c_qlog),                           # 0x0008
        ("Log2", c_qlog),                           # 0x0A9C
        ("Log3", c_qlog),                           # 0x1530
        ("unk1", ctypes.c_uint8 * 0x38),            # 0x1FC4
        ("Checksum", ctypes.c_uint32)               # 0x1FFC
    ]

    def recalculate_checksums(self):
        self.Log1.recalculate_checksum()
        self.Log2.recalculate_checksum()
        self.Log3.recalculate_checksum()
        self.Checksum = dat_checksum(bytes(self)[:(ctypes.sizeof(c_dat) - ctypes.sizeof(ctypes.c_uint32))])

assert(ctypes.sizeof(c_dat) == 0x2000)

class c_info(ctypes.BigEndianStructure): # Size: 0xF38
    _pack_ = 1
    _fields_ = [
        ("Savedata", c_save),                       # 0x000
        ("Memory", c_memory),                       # 0x958
        ("Dan", c_danbit),                          # 0x978
        ("Zone", c_zone * 32),                      # 0x9B4
        ("Restart", c_restart),                     # 0xDB4
        ("Tmp", c_event),                           # 0xDD8
        ("TurnRestart", c_turnrestart),             # 0xED8
        ("field_0xf14", ctypes.c_uint8 * 4),        # 0xF14
        ("DataNum", ctypes.c_uint8),                # 0xF18
        ("NewFile", ctypes.c_uint8),                # 0xF19
        ("NoFile", ctypes.c_uint8),                 # 0xF1A
        ("field_0xf1b", ctypes.c_uint8 * 13),       # 0xF1B
        ("StartTime", ctypes.c_int64),              # 0xF28
        ("SaveTotalTime", ctypes.c_int64),          # 0xF30
    ]
assert(ctypes.sizeof(c_info) == 0xF38)


class c_event_flag(ctypes.BigEndianStructure): # Size: 0x66C
    _pack_ = 1
    _fields_ = [
        ("saveBitLabels", ctypes.c_uint16 * 822),   # 0x00
    ]
assert(ctypes.sizeof(c_event_flag) == 0x66C)


class c_event_tmp_flag(ctypes.BigEndianStructure): # Size: 0x172
    _pack_ = 1
    _fields_ = [
        ("tempBitLabels", ctypes.c_uint16 * 185),   # 0x00
    ]
assert(ctypes.sizeof(c_event_tmp_flag) == 0x172)

