connectivity_plan = {
    "5GB": 85000,
    "10GB": 135000,
    "20GB": 240000,
    "30GB": 345000,
    "50GB": 560000,
    "75GB": 822000,
    "100GB": 1085000,
    "150GB": 1625000,  # Artificial
    "200GB": 2165000,  # Artificial
    "250GB": 2712500,  # Artificial
    "300GB": 3255000,  # Artificial
    "350GB": 3797500,  # Artificial
    "400GB": 4340000,  # Artificial
    "450GB": 4882500,  # Artificial
    "500GB": 5305000,
    "550GB": 5837500,  # Artificial
    "600GB": 6510000,  # Artificial
    "700GB": 7595000,  # Artificial
    "750GB": 7942000,
    "800GB": 8680000,  # Artificial
    "850GB": 9222500,  # Artificial
    "900GB": 9765000,  # Artificial
    "1000GB": 10579000
}

cloud_plan = {
    "Amazon Web Service - EC2 Shared Server": 1000000,
    "Amazon Web Service - EC2 Dedicated Server": 21160203
}

appliance_managed_service = {
    "Kecilin - Appliance Managed Service": 14400000,
}

# Define fixed colors for each category
color_discrete_map = {
    "CCTV": "#D3D3D3",
    "NVR/DVR": "#8772FC",
    "Installation": "#383838",
    "Platform": "#001A41",
    "License": "#92C0DF",
    "Cloud": "#B90024",
    "Connectivity": "#DC0E04",
    "Managed Service": "#FDA22B"
}

# Data usage for each resolution level
data_usage = {
    "1MP": {"daily": 8, "monthly": 240},
    "2MP": {"daily": 17, "monthly": 510},
    "3MP": {"daily": 25, "monthly": 750},
    "4MP": {"daily": 34, "monthly": 1020},
    "5MP": {"daily": 42, "monthly": 1260},
    "6MP": {"daily": 51, "monthly": 1530},
    "7MP": {"daily": 59, "monthly": 1770},
    "8MP": {"daily": 68, "monthly": 2040},
    "12MP": {"daily": 102, "monthly": 3060}
}

# Define compression hardware
compression_hardware = {
    'Nvidia Jetson Orin Nano 8 GB': 14000000,
    'Nvidia Jetson AGX Orin 32 GB': 37500000,
    'Nvidia Jetson AGX Orin 64 GB': 62455000
}