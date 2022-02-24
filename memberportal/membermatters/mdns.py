import socket
import time
from zeroconf import IPVersion, ServiceInfo, Zeroconf, InterfaceChoice


def run():
    try:
        zeroconf = Zeroconf(ip_version=IPVersion.All, interfaces=InterfaceChoice.All)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ip = s.getsockname()[0]

        info = ServiceInfo(
            "_http._tcp.local.",
            "Member Matters Server._http._tcp.local.",
            addresses=[socket.inet_aton(ip)],
            properties={"ip": ip},
            port=80,
            server="membermatters.local.",
        )

        zeroconf.register_service(info)
    except:
        pass

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()


if __name__ == "__main__":
    run()
