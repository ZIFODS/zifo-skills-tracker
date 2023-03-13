/**
 * Convert Consultant names to initials.
 *
 * @param {string} name Name of consultant.
 * @return {string} Initials of consultant.
 */
export function consultantInitials(name: string): string {
  let initials = "";
  const splitWords = name.trim().split(" ");
  splitWords.forEach((word) => {
    initials += word[0].toUpperCase();
  });
  return initials;
}
