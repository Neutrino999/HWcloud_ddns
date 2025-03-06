from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkdns.v2 import *
from huaweicloudsdkdns.v2.region.dns_region import DnsRegion
from huaweicloudsdkcore.exceptions import exceptions
import os

# 从环境变量获取敏感信息，确保安全性
ak = os.getenv('HUAWEICLOUD_SDK_AK')
sk = os.getenv('HUAWEICLOUD_SDK_SK')
project_id = "your_project_id"  # 项目 ID
region = 'cn-north-4'  # 区域

if not all([ak, sk, project_id]):
    raise ValueError("请设置环境变量 HUAWEICLOUD_SDK_AK, HUAWEICLOUD_SDK_SK, HUAWEICLOUD_SDK_PROJECT_ID")

credentials = BasicCredentials(ak, sk, project_id=project_id)

client = DnsClient.new_builder() \
    .with_credentials(credentials) \
    .with_region(DnsRegion.value_of(region)) \
    .build()

# 获取公网域名的 zone_id
try:
    request = ListPublicZonesRequest()
    response = client.list_public_zones(request)

    zones = response.zones  # 获取区域列表
    with open('ids.txt', 'w', encoding='utf-8') as f:
        for zone in zones:
            f.write(f"Zone Name: {zone.name}, Zone ID: {zone.id}\n")

            # 获取该 zone 内的 recordset_id
            recordset_request = ListRecordSetsRequest()
            recordset_request.zone_id = zone.id
            recordset_response = client.list_record_sets(recordset_request)

            recordsets = recordset_response.recordsets
            for recordset in recordsets:
                f.write(f"  Recordset Name: {recordset.name}, Recordset ID: {recordset.id}\n")
except exceptions.ClientRequestException as e:
    with open('ids.txt', 'a', encoding='utf-8') as f:
        f.write("请求异常：\n")
        f.write(f"状态码：{e.status_code}\n")
        f.write(f"请求ID：{e.request_id}\n")
        f.write(f"错误信息：{e.error_msg}\n")
except exceptions.SdkException as e:
    with open('ids.txt', 'a', encoding='utf-8') as f:
        f.write("SDK 异常：\n")
        f.write(str(e) + '\n')