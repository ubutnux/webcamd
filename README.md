# BRT Cam

`webcamd` is based on Igor Maculan’s *“Simple Python Motion Jpeg”* [daemon](https://gist.github.com/n3wtron/4624820). It has been reworked to run under python-3.x, accept command-line arguments, to fine-tune the webcam streaming experience.

### Note!

The user running `webcamd` must have sufficient access to the webcam device. On most Linux systems, this is as simple as adding the user to the `video` group. Otherwise the daemon will have to be run as root, which is **NOT** recommended.

webcam@.service is a systemd unit file for webcam.py.

haproxy.cfg is a configuration file for haproxy that actually works with non-ancient versions of haproxy, and enforces SSL connections to Octoprint.

***

# `webcamd` Quickstart

### Install Locally

`$` `pip install .`


### Run the module directly

`$` `python3 -m webcamd`

### Help and Usage

`$` `webcamd --help`


### Create a SystemD Service

Open the following file and copy these contents:

```
/etc/systemd/system/webcamd.service
___________________________________
[Unit]
Description=Webcam Daemon. A minimalist webcam streaming service.
After=network.online.target
Wants=network.online.target

[Service]
Type=simple
User=brt
Group=brt
ExecStart=/usr/local/bin/webcamd
ExecStop=killall -u webcam webcamd

[Install]
WantedBy=multi-user.target
```

Then restart the systemd daemon loader:

`$` `sudo systemctl daemon-reload`

And enable the service, to allow the service to start automatically on boot:

`$` `sudo systemctl enable webcamd.service`

***

# Development

### Install Locally with `dev` dependencies

`$` `pip install -e .[dev]`

***

&nbsp;

# Contributors and Authors

This repository is a derevation of the [octoprint-stuff repo](https://github.com/christopherkobayashi/octoprint-stuff) maintained by Christopher RYU and Shell Shrader. The specific webcampy script that inspired this repository was originally authored by Igor Maculan.
