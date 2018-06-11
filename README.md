== installation

Move graphite2http.py in /opt/

Move graphite2http.service in /etc/systemd/system/

Create a config file /etc/graphite2http.cfg:
```
[general]
token=<your token>
key=<your key>
```

Register service in systemd:

```systemctl daemon-reload```

Enable service:

```systemctl enable graphite2http```

You can now send metrics to port 2003, they will be forwarded to graphapi.lunasys.fr
