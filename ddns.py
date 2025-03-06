# coding: utf-8

import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkdns.v2.region.dns_region import DnsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkdns.v2 import *

if __name__ == "__main__":
    ak = os.environ["HUAWEICLOUD_SDK_AK"]
    sk = os.environ["HUAWEICLOUD_SDK_SK"]

    credentials = BasicCredentials(ak, sk)

    client = DnsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(DnsRegion.value_of("cn-north-4")) \
        .build()

    try:
        zone_id = "your_zone_id" # 设置域名 ID
        recordset_id = "your_recordset_id" # 设置记录集 ID
        request = UpdateRecordSetRequest()
        request.zone_id = zone_id  # 设置 zone_id
        request.recordset_id = recordset_id  # 设置记录集 ID
        with open("ip.txt", "r") as file:
            ip_address = file.read().strip()
        listRecordsbody = [ip_address]
        request.body = UpdateRecordSetReq(
            records=listRecordsbody,
            ttl=300,
            type="A",
            description="Update A record for ddns.hwxbox.cn",
            name="a.example.com."
        )
        response = client.update_record_set(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)