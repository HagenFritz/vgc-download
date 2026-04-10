from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vgc-download")


@mcp.tool()
async def fetch_usage_stats(format: str = "gen9vgc2025") -> str:
    """Fetch current usage statistics from Pokemon Showdown for a given format."""
    # TODO: implement
    return f"Usage stats for {format} — not yet implemented"


@mcp.tool()
async def get_pokemon_data(pokemon: str) -> str:
    """Look up base stats, abilities, notable moves, and typing for a Pokemon."""
    # TODO: implement
    return f"Data for {pokemon} — not yet implemented"


@mcp.tool()
async def validate_team(team_file: str = "data/my_team.json") -> str:
    """Validate a team file against current season rules."""
    # TODO: implement
    return f"Validation for {team_file} — not yet implemented"


if __name__ == "__main__":
    mcp.run(transport="stdio")
