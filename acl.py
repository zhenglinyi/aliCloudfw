# encoding=utf-8
import warnings
import json
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

warnings.filterwarnings(action='ignore', module='urllib3')
LOG = logging.getLogger(__name__)


class Cloudfw(object):

    #填写你的accessKeyId和accessSecret
    def __init__(self):
        self.accessKeyId=''
        self.accessSecret=''
        self.region='cn-hangzhou'


    def initRequest(self):
        client = AcsClient(self.accessKeyId, self.accessSecret, self.region)

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('cloudfw.cn-hangzhou.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-12-07')
        return client,request
    #下发策略
    def sync(self):
        try:
            client,request=self.initRequest();
            request.set_action_name('AddControlPolicy')

            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('AclAction', "accept")
            request.add_query_param('ApplicationName', "ANY")
            request.add_query_param('Description', "demo1")
            request.add_query_param('Destination', "1.2.3.0/24")
            request.add_query_param('DestinationType', "net")
            request.add_query_param('Direction', "in")
            request.add_query_param('Proto', "ANY")
            request.add_query_param('Source', "1.2.3.0/24")
            request.add_query_param('SourceType', "net")
            request.add_query_param('NewOrder', "-1")
            request.add_query_param('SourceIp', "10.3.5.169")
            request.add_query_param('Lang', "zh")
            request.add_query_param('Release', "true")

            response = client.do_action_with_exception(request)
            print(str(response, encoding='utf-8'))
            return json.loads(response)["AclUuid"]
        except Exception as e:
            LOG.error(e, exc_info=True)

    #修改策略
    def modify_acl(self, aclUuid,description=""):
        try:

            client,request=self.initRequest();
            request.set_action_name('ModifyControlPolicy')

            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('AclAction', "accept")
            request.add_query_param('ApplicationName', "ANY")
            request.add_query_param('Description', description)
            request.add_query_param('Destination', "1.2.3.0/24")
            request.add_query_param('DestinationType', "net")
            request.add_query_param('Direction', "in")
            request.add_query_param('Proto', "ANY")
            request.add_query_param('Source', "1.2.3.0/24")
            request.add_query_param('AclUuid', aclUuid)
            request.add_query_param('SourceType', "net")
            request.add_query_param('Lang', "zh")
            request.add_query_param('Release', "true")

            response = client.do_action_with_exception(request)
            print(str(response, encoding='utf-8'))
            return json.loads(response)
        except Exception as e:
            LOG.error(e, exc_info=True)

    # 删除策略
    def delete_acl(self, aclUuid):
        try:
            client,request=self.initRequest();
            request.set_action_name('DeleteControlPolicy')

            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('AclUuid', aclUuid)
            request.add_query_param('Direction', "in")
            request.add_query_param('Lang', "zh")
            response = client.do_action(request)
            # python2:  print(response)
            print(str(response, encoding='utf-8'))
            return json.loads(response)
        except Exception as e:
            LOG.error(e, exc_info=True)

    #获取所有访问控制策略的信息
    def get_acl_describe(self,aclUuid=""):
        try:
            client,request=self.initRequest();
            request.set_action_name('DescribeControlPolicy')

            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('Direction', "in")
            request.add_query_param('CurrentPage', "1")
            request.add_query_param('PageSize', "10")
            request.add_query_param('Lang', "zh")
            request.add_query_param('Source', "1.2.3.0/24")
            request.add_query_param('Destination', "1.2.3.0/24")
            request.add_query_param('Description', "test")
            request.add_query_param('Proto', "ANY")
            request.add_query_param('AclAction', "accept")
            request.add_query_param('Release', "true")
            if aclUuid!="":
                request.add_query_param('AclUuid', aclUuid)

            response = client.do_action(request)
            # python2:  print(response)
            print(str(response, encoding='utf-8'))
            return json.loads(response)
        except Exception as e:
            LOG.error(e, exc_info=True)

    #查询访问控制策略优先级生效范围
    def get_prior(self):
        try:
            client, request = self.initRequest();
            request.set_action_name('DescribePolicyPriorUsed')

            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('Direction', "in")

            response = client.do_action(request)
            res = json.loads(response)
            #print(res["Start"])
            # python2:  print(response)
            print(str(response, encoding='utf-8'))
            return res["Start"],res["End"]
        except Exception as e:
            LOG.error(e, exc_info=True)

    #修改访问控制策略的优先级
    def modify_prior(self,newOrder,oldOrder):
        try:
            client, request = self.initRequest();
            request.set_action_name('ModifyControlPolicyPosition')

            request.add_query_param('RegionId', "cn-hangzhou")
            request.add_query_param('Direction', "in")
            request.add_query_param('NewOrder', newOrder)
            request.add_query_param('OldOrder', oldOrder)

            response = client.do_action(request)
            # python2:  print(response)
            print(str(response, encoding='utf-8'))

            return json.loads(response)
        except Exception as e:
            LOG.error(e, exc_info=True)


if __name__ == "__main__":
    cf = Cloudfw()
    cf.sync()
    #cf.get_prior()
