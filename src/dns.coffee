#!/usr/bin/env coffee --compile
# run this file to compile it

ndns = require "./ndns" # available via npm

# Blidingly copying to make something work on my computer.

lookup = console.log

class DnsServer extends ndns.Server
    constructor: ->
        super "udp4"
        @pattern = /(\.|^)jeb\.?$/
        @on "request", @handleRequest
        
    listen: (port, callback) ->
        @bind port
        callback?()
    
    handleRequest: (req, res) =>
        res.header = req.header
        res.question = req.question
        res.header.aa = 1
        res.header.qr = 1
        
        q = req.question[0] ? {}
        
        if q.type is ndns.ns_t.a and q.class is ndns.ns_c.in and @pattern.test q.name
            resIp = lookup(q.name)
            res.addRR ndns.ns_s.an, q.name, ndns.ns_t.a, ndns.ns_c.in, 600, resIP
        else
            res.header.rcode = ndns.ns_rcode.nxdomain
        
        res.send()

new DnsServer