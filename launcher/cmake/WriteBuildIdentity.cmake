# Runs before compilation on every build, including incremental builds.
set(SOURCE_COMMIT "unknown")
set(SOURCE_DIRTY true)
# The source may be a subdirectory of a larger repository, so ask git rather
# than looking for .git here. Requiring one of this directory's own files to be
# tracked keeps an archive unpacked inside an unrelated repository "unknown".
set(tracked_result 1)
if(GIT_EXECUTABLE)
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${SOURCE_DIR}" ls-files --error-unmatch cmake/BuildIdentity.h.in
    OUTPUT_QUIET ERROR_QUIET RESULT_VARIABLE tracked_result)
endif()
if(tracked_result EQUAL 0)
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${SOURCE_DIR}" rev-parse HEAD
    OUTPUT_VARIABLE commit OUTPUT_STRIP_TRAILING_WHITESPACE RESULT_VARIABLE commit_result)
  # Only changes under the source directory make the build dirty.
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${SOURCE_DIR}" status --porcelain --untracked-files=normal -- .
    OUTPUT_VARIABLE changes RESULT_VARIABLE status_result)
  if(commit_result EQUAL 0 AND status_result EQUAL 0 AND commit MATCHES "^[0-9a-f]+$")
    set(SOURCE_COMMIT "${commit}")
    if(changes STREQUAL "")
      set(SOURCE_DIRTY false)
    endif()
  endif()
endif()
set(BUILD_SOURCE "${SOURCE_COMMIT}")
if(SOURCE_DIRTY)
  string(APPEND BUILD_SOURCE "-dirty")
endif()
file(MAKE_DIRECTORY "${OUTPUT_DIR}")
configure_file("${SOURCE_DIR}/cmake/BuildIdentity.h.in" "${OUTPUT_DIR}/BuildIdentity.h" @ONLY)
configure_file("${SOURCE_DIR}/cmake/source.json.in" "${OUTPUT_DIR}/source.json" @ONLY)
