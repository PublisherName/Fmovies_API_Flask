''' This module contains the routes for the fmoviesz package. '''
from flask import jsonify, request
from .search_by_name import search_by_name_bp, scrap_fmoviesz_by_name


@search_by_name_bp.route('/media/searchByName', methods=['GET'])
def search_media():
    '''Search for media by title.'''
    name = request.args.get('name', default='')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    media = scrap_fmoviesz_by_name(name)
    return jsonify(media), 200
