#include "settings.h"
#include <stdio.h>

int main(int argc, char** argv)
{
	if (argc == 1)
	{
		printf("VERSION %d.%d.%d", bfgame_VERSION_MAJOR, bfgame_VERSION_MINOR, bfgame_VERSION_PATCH);
		return -1;
	}
	return 0;
}
