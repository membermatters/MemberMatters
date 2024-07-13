import { z } from 'zod';

export const MemberbucksTransactionsTypeSchema = z.enum([
  'stripe',
  'other',
  'interlock',
  'card',
  'web',
]);

export type MemberbucksTransactionsType = z.infer<
  typeof MemberbucksTransactionsTypeSchema
>;
