# credit https://gist.github.com/robere2/88af445d2285682fed9f5c001f30b186
# converted above to python and modified to work in this context

ranks = {
    "ADMIN": [
        [
            'c',
            "[ADMIN]"
        ]
    ],
    "MODERATOR": [
        [
            '2',
            "[MOD]"
        ]
    ],
    "HELPER": [
        [
            '9',
            "[HELPER]"
        ]
    ],
    "JR_HELPER": [
        [
            '9',
            "[JR HELPER]"
        ]
    ],
    "YOUTUBER": [
        [
            'c',
            "["
        ],
        [
            'f',
            "YOUTUBE"
        ],
        [
            'c',
            "]"
        ]
    ],
    "SUPERSTAR": [
        [
            "ffaa00",
            "[MVP"
        ],
        [
            "%p",
            "++"
        ],
        [
            "%r",
            "]"
        ]
    ],
    "MVP_PLUS": [
        [
            '3ce6e6',
            "[MVP"
        ],
        [
            "%p",
            "+"
        ],
        [
            'b',
            "]"
        ]
    ],
    "MVP": [
        [
            '3ce6e6',
            "[MVP]"
        ]
    ],
    "VIP_PLUS": [
        [
            '3ffe3f',
            "[VIP"
        ],
        [
            'd9a334',
            "+"
        ],
        [
            'a',
            "]"
        ]
    ],
    "VIP": [
        [
            '3ffe3f',
            "[VIP]"
        ]
    ],
    "DEFAULT": [
        [
            '6e6b6b',
            ""
        ]
    ]
}

colors = {
    "BLACK": '000000',
    "DARK_BLUE": '0000be',
    "DARK_GREEN": '00be00',
    "DARK_AQUA": '00bebe',
    "DARK_RED": 'be0000',
    "DARK_PURPLE": 'be00be',
    "GOLD": 'd9a334',
    "GRAY": 'bebebe',
    "DARK_GRAY": '3f3f3f',
    "BLUE": '3f3ffe',
    "GREEN": '3ffe3f',
    "AQUA": '3ffefe',
    "RED": 'fe3f3f',
    "LIGHT_PURPLE": 'fe3ffe',
    "YELLOW": 'fefe3f',
    "WHITE": 'ffffff'
}

default_plus_color = 'fe3f3f'
default_rank_color = 'd9a334'

def calc_tag(player):
    if player and isinstance(player, dict):
        # In order of least priority to highest priority
        package_rank = player.get('packageRank')
        new_package_rank = player.get('newPackageRank')
        monthly_package_rank = player.get('monthlyPackageRank')
        rank_plus_color = player.get('rankPlusColor')
        monthly_rank_color = player.get('monthlyRankColor')
        rank = player.get('rank')
        prefix = player.get('prefix')

        if rank == "NORMAL":
            rank = None
        if monthly_package_rank == "NONE":
            monthly_package_rank = None
        if package_rank == "NONE":
            package_rank = None
        if new_package_rank == "NONE":
            new_package_rank = None

        if prefix and isinstance(prefix, str):
            return parse_minecraft_tag(prefix)
        if rank or monthly_package_rank or new_package_rank or package_rank:
            return replace_custom_colors(
                ranks.get(rank or monthly_package_rank or new_package_rank or package_rank, ranks["DEFAULT"]),
                colors.get(rank_plus_color),
                colors.get(monthly_rank_color)
            )
    return replace_custom_colors(ranks["DEFAULT"], None, None)

def parse_minecraft_tag(tag):
    if tag and isinstance(tag, str):
        new_rank = []

        split_tag = tag.split(r'§([a-f0-9])', tag)
        split_tag.insert(0, 'f')  # Beginning is always going to be white (typically empty though)

        for i in range(len(split_tag)):
            j = i // 2  # First index
            k = i % 2   # Second index

            if len(new_rank) <= j:
                new_rank.append([])
            if len(new_rank[j]) <= k:
                new_rank[j].append('')
            new_rank[j][k] = split_tag[i]

        return new_rank
    else:
        return [['f', '']]

def replace_custom_colors(rank, p, r):
    if not isinstance(rank, list):
        return rank

    new_rank = [list(component) for component in rank]

    """if not p or not isinstance(p, str) or len(p) > 1:
        p = default_plus_color
    if not r or not isinstance(r, str) or len(r) > 1:
        r = default_rank_color"""

    for component in new_rank:
        if isinstance(component, list) and len(component) >= 2:
            if component[0] == "%p":
                component[0] = p
            if component[0] == "%r":
                component[0] = r

    if new_rank[1][0] == None:
        new_rank[1][0] = 'fe3f3f'

    return new_rank


