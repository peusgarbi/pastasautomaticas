from pathlib import Path
import subprocess
import ctypes
import sys


SYNCHRONIZE = 0x00100000
INFINITE = 0xFFFFFFFF


def wait_process_exit(pid: int):
    """
    Aguarda o processo informado encerrar utilizando a API do Windows.
    """

    kernel32 = ctypes.windll.kernel32

    handle = kernel32.OpenProcess(
        SYNCHRONIZE,
        False,
        pid,
    )

    if handle:
        kernel32.WaitForSingleObject(
            handle,
            INFINITE,
        )

        kernel32.CloseHandle(handle)


def main():
    if len(sys.argv) != 4:
        print("Uso: updater.exe <pid> <executavel_atual> <novo_executavel>")
        sys.exit(1)

    pid = int(sys.argv[1])
    current_exe = Path(sys.argv[2])
    new_exe = Path(sys.argv[3])
    backup_exe = current_exe.with_suffix(".bak")

    #
    # Aguarda o programa principal encerrar
    #

    wait_process_exit(pid)

    #
    # Remove backup antigo
    #

    if backup_exe.exists():
        backup_exe.unlink()

    try:
        #
        # Cria backup do executável atual
        #
        current_exe.rename(
            backup_exe,
        )
        #
        # Instala a nova versão
        #
        new_exe.replace(
            current_exe,
        )
    except Exception:
        #
        # Restaura o executável anterior
        #
        if backup_exe.exists() and not current_exe.exists():
            backup_exe.replace(
                current_exe,
            )
        raise

    #
    # Reinicia o programa
    #

    subprocess.Popen(
        [str(current_exe)],
        cwd=current_exe.parent,
    )


if __name__ == "__main__":
    main()
