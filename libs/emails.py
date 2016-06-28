# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function
import requests
import ewsclient
import ewsclient.monkey
import suds.client
from suds.transport.https import WindowsHttpAuthenticated
from django.conf import settings


def send_email(to_email, subject="", html="", from_email="zoneke.ccy@gmail.com", files=None, **kwargs):
    #send_email_by_sendcloud(to_email, subject, html, from_email, **kwargs)
    bcc = settings.EMAIL_TO
    kwargs['bcc'] = bcc
    return send_email_by_mailgun(to_email, subject, html, from_email, files=files, **kwargs)


def send_email_by_sendcloud(to_email, subject="", html="", from_email="zoneke.ccy@gmail.com", files=None, **kwargs):
    url = "https://sendcloud.sohu.com/webapi/mail.send.xml"
    params = {
        "api_user": "postmaster@zoneke.sendcloud.org",
        "api_key": "Rdtk4b9f",
        "from": from_email,
        "to": to_email,
        "subject": subject,
        "html": html,
        }
    params.update(kwargs)
    return requests.post(url, data=params)


def send_email_by_mailgun(to_email, subject, html, from_email="zoneke.ccy@gmail.com", files=None, **kwargs):
    data = {"from": from_email,
            "to": to_email.split(";"),
            "subject": subject,
            "html": html}
    data.update(kwargs)
    if files:
        return requests.post(
            "https://api.mailgun.net/v2/zoneke.com/messages",
            auth=("api", "key-1t13ykjl8haxzxlxo99q4aoraj3u8hk2"),
            data=data,
            files=files
        )
    return requests.post(
        "https://api.mailgun.net/v2/zoneke.com/messages",
        auth=("api", "key-1t13ykjl8haxzxlxo99q4aoraj3u8hk2"),
        data=data
    )


class Email():
    '''
    eg:
        e = Email()
        e.send(["xx@qq.com",xx@qq.com"], '邮件标题', '邮件内容')
    '''

    def __init__(self):
        domain = settings.EMAIL_HOST
        username = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD

        transport = WindowsHttpAuthenticated(username=username,
            password=password)
        self.client = suds.client.Client("https://%s/EWS/Services.wsdl" % domain,
            transport=transport,
            plugins=[ewsclient.AddService()])

    def send(self, to_list, subject, content):
        email_address = u'''<t:Mailbox><t:EmailAddress>%s</t:EmailAddress></t:Mailbox>'''
        to = "".join([email_address % email for email in to_list])
        if not isinstance(subject, unicode):
            subject = unicode(subject, "utf-8")
        if not isinstance(content, unicode):
            content = unicode(content, "utf-8")

        xml = u'''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
                  <soap:Body>
                    <CreateItem MessageDisposition="SendAndSaveCopy" xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
                      <SavedItemFolderId>
                        <t:DistinguishedFolderId Id="sentitems" />
                      </SavedItemFolderId>
                      <Items>
                        <t:Message>
                          <t:ItemClass>IPM.Note</t:ItemClass>
                          <t:Subject><![CDATA[%s]]></t:Subject>
                          <t:Body BodyType="HTML"><![CDATA[%s]]></t:Body>
                          <t:ToRecipients>
                            %s
                          </t:ToRecipients>
                        </t:Message>
                      </Items>
                    </CreateItem>
                  </soap:Body>
                </soap:Envelope>''' % (subject, content, to)
        logger.info(xml)
        try:
            self.client.service.CreateItem(__inject={u'msg': xml})
            return True
        except Exception, e:
            logger.exception(u"邮件发送失败！%s %s %s" % (to_list, subject, content))
            return False


def test():
    from_email = "zoneke.ccy@gmail.com"
    to_email = "xutao03@gmail.com"
    subject = "这是测试邮件"
    html = "Hello World"
    send_email(from_email, to_email, subject, html)