# from flask import Flask, Blueprint, render_template, request, jsonify
# #
# # from app import TokenParser
# '''
#     USE render_template to render HTML files in FLASK FILESYSTEM
#     USE {{ }} IN HTML TO RENDER VARIABLES FROM FLASK
#     USE {% %} TO RENDER CODE BLOCKS
#
# '''
#
# views = Blueprint(__name__, 'views')
#
#
#
# ''' SIMPLE PAGE TO DISPLAYS WEBHOOK (HTTML)'''
# @views.route('/web')
# def index():
#     #token = TokenParser.get_access_token
#     return render_template('index.html',
#                            TITLE="WEBHOOK",
#                            CONTENT="This is a webhook",
#                             TOKEN = "token"
#                            )
#
# '''
#     CREATES A DYNAMIC WEBPAGE THAT DISPLAYS (AND CHANGES) BASED OFF OF WHAT IS INSIDE OF URL
#     EXAMPLE: http://localhost:5000/web/web/change/1234
#     WILL DISPLAY: 1234 IN TITLE
# '''
# @views.route('/web/change/<string:ID>')
# def pageByID(ID):
#     return render_template ("index.html",
#                             TITLE=ID,
#                             CONTENT="This is a webhook")
#
# '''
#     PASSES A QUERY [?] PARAMATER TO THE URL
#     IT PULLS THE QUERY PARAMATER AND DISPLAYS IT ON THE PAGE
#     EXAMPLE: http://localhost:5000/web/query?name=FUAD --- *refer: [?]name=FUAD)
#     WILL DISPLAY: FUAD IN TITLE
#
#     USAGE: 'args' is a dictionary that contains all the query parameters in the URL
# '''
#
# @views.route('/search/query')
# def get_query_param():
#     args = request.args
#     id = request.args.get('TOKEN')
#     return render_template("index.html",
#                            TITLE=id,
#                            CONTENT="This is a webhook")
#
#
