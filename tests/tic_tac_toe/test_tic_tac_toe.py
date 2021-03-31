import http

from tests import constants
from tests.tic_tac_toe.utils import get_board_filled_cell
from tests.validators import validate_error_msg, validate_type
from tic_tac_toe.constants import PLAYER_VALUE
from tic_tac_toe.enums import TicTacToeErrors
from tic_tac_toe.services.tic_tac_toe import tic_tac_toe_service


class TestTicTacToeGame:

    @staticmethod
    def get_game_patch_url(game_id: int) -> str:
        return f'{constants.Urls.tic_tac_toe.value}{game_id}/'

    @staticmethod
    def get_game_get_stats_url(game_id: int) -> str:
        return constants.Urls.tic_tac_toe_stats.value.format(id=game_id)

    @staticmethod
    def get_valid_payload(board):
        row, col = tic_tac_toe_service.get_move_coordinates(board, PLAYER_VALUE)
        payload = {'col': col, 'row': row}
        return payload

    async def test_create_game_without_user_error(self, api_client):
        response = await api_client.post(constants.Urls.tic_tac_toe.value)
        assert response.status == http.HTTPStatus.UNAUTHORIZED

    async def test_create_game_success(self, api_client, token_hdr):
        response = await api_client.post(constants.Urls.tic_tac_toe.value, headers=token_hdr)
        assert response.status == http.HTTPStatus.OK
        response_data = await response.json()
        assert True is response_data['active']

    async def test_game_step_process_success(self, api_client, token_hdr, game):
        initial_depth = len(tic_tac_toe_service._empty_cells(game['field']['board']))
        payload = self.get_valid_payload(game['field']['board'])
        response = await api_client.patch(self.get_game_patch_url(game['id']), headers=token_hdr, json=payload)
        assert response.status == http.HTTPStatus.OK
        response_data = await response.json()
        depth = len(tic_tac_toe_service._empty_cells(response_data['field']['board']))
        # initial_depth - 2 - because player and computer make moves
        assert initial_depth - 2 == depth

    async def test_game_step_fill_non_empty_cell_error(self, api_client, token_hdr, game_with_step):
        row, col = get_board_filled_cell(game_with_step['field']['board'])
        payload = {'col': col, 'row': row}
        response = await api_client.patch(
            self.get_game_patch_url(game_with_step['id']), headers=token_hdr, json=payload)
        await validate_error_msg(response, TicTacToeErrors.invalid_turn.value)

    async def test_game_step_on_finished_game_error(self, api_client, token_hdr, finished_game):
        payload = {'col': 0, 'row': 0}
        response = await api_client.patch(self.get_game_patch_url(finished_game['id']), headers=token_hdr, json=payload)
        await validate_error_msg(response, TicTacToeErrors.game_already_over.value)

    async def test_game_step_non_user_game_error(self, api_client, game_with_step, token_hdr, token_hdr2):
        payload = self.get_valid_payload(game_with_step['field']['board'])
        response = await api_client.patch(
            self.get_game_patch_url(game_with_step['id']),
            headers=token_hdr2,
            json=payload
        )
        await validate_error_msg(response, TicTacToeErrors.not_user_game.value)

    async def test_game_step_with_invalid_id_error(self, api_client, token_hdr, game_with_step):
        payload = self.get_valid_payload(game_with_step['field']['board'])
        response = await api_client.patch(self.get_game_patch_url(-1), headers=token_hdr, json=payload)
        assert response.status == http.HTTPStatus.NOT_FOUND

    async def test_game_stats_success(self, api_client, token_hdr, finished_game):
        response = await api_client.get(self.get_game_get_stats_url(finished_game['id']), headers=token_hdr)
        response_data = await response.json()
        exp_stat_entity = {
            'created_at': validate_type(str),
            'field': validate_type(dict)
        }
        for game_stat in response_data:
            assert exp_stat_entity == game_stat

    async def test_game_stats_with_invalid_id_error(self, api_client, token_hdr, finished_game):
        response = await api_client.get(self.get_game_get_stats_url(-1), headers=token_hdr)
        assert response.status == http.HTTPStatus.NOT_FOUND
