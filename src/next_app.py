import os

# Default values
cur_app = 0
total_apps = 1
pi_sugar=True

def write_glance_config():
    configs = [
        f"page={cur_app}",
        f"numofapps={total_apps}",
        f"has_pi_sugar={pi_sugar}",
    ]
    with open("glance.conf", "w") as glance_file:
        for config in configs:
            glance_file.write(config)
            glance_file.write("\n")

if not os.path.exists("glance.conf"):
    write_glance_config()
else:
    with open("glance.conf") as glance_conf:
        for row in glance_conf:
            key, value = row.split("=")
            if key == "page":
                cur_app = int(value)
            elif key == "numofapps":
                total_apps = int(value)
            elif key == "has_pi_sugar":
                pi_sugar = bool(value)

cur_app = (cur_app + 1) % total_apps
write_glance_config()
